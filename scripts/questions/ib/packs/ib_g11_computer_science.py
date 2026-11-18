"""IB DP Computer Science (new guide, first assessment May 2027) – ib-g11-computer-science.

Year-1 content: A1 Computer fundamentals, A2 Networks (Paper 1, Theme A) and B1 Computational thinking,
B2 Programming (Paper 2, Theme B).

Numerical and tracing items are parametric and their answers are COMPUTED here:
  * number bases, two's complement, file sizes and compression are calculated,
  * logic expressions are evaluated over every input row; simplification uses sympy,
  * CPU (fetch-decode-execute), caches, schedulers, deadlock graphs and control loops are simulated,
  * subnetting uses the ipaddress module, routing uses Dijkstra, ciphers/hashes are executed,
  * programming items generate Python (and IB-style pseudocode) and exec() it to capture the real output;
    file-processing items run against an in-memory file system.
"""
from __future__ import annotations

import hashlib
import heapq
import ipaddress
import itertools
import math
from collections import deque

from _common import F, Registry, T, mcq, name, CITIES
from ib_cs_common import Kit, run_py, table, r2, code_q, PEOPLE

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# HL papers: Paper 1 (Theme A + case study) 2 h, 80 marks = Section A 56 + case study 24 (4 challenge
# questions); Paper 2 (Theme B, Java or Python) 2 h, 80 marks. One mock = both papers, 22 questions, 160 marks.
MOCK = [
    dict(section='Paper 1 Section A – Theme A structured questions (computer fundamentals, networks)', count=8,
         c=['C3', 'C4', 'C3', 'C4'], d=[3, 4, 3, 5], type='multi_step', marks=7, style='structured', chapters=[1, 2, 3, 4, 5, 6, 7]),
    dict(section='Paper 1 Section B – Case study challenge questions', count=4,
         c=['C4'], d=[4, 5, 4], type='long', marks=6, style='case_study', chapters=[1, 2, 3, 4, 5, 6, 7]),
    dict(section='Paper 2 – Theme B structured programming questions (computational thinking, Python/Java)', count=10,
         c=['C3', 'C4', 'C3'], d=[3, 4, 5, 3], type='multi_step', marks=8, style='structured', chapters=[8, 9, 10, 11, 12]),
]

STYLE = {'eval_marks': 6, 'essay_marks': 8,
         'markband': 'top band: well-balanced discussion with accurate, specific technical detail applied to the context and a justified conclusion; '
                     'middle band: some balance and correct terminology, conclusion only partly supported; '
                     'bottom band: descriptive, largely one-sided, little technical detail or application.'}

R = Registry()

CASE_ORGS = [
    'Ruta Verde, a logistics company in Monterrey, tracks 400 delivery vans with GPS units, runs route planning on cloud servers and connects three depots through a VPN.',
    'Kibera Learning Hub, a community school in Nairobi, has a computer lab of 30 thin clients, a small file server and an unreliable internet connection shared by staff and students.',
    'Harbour Health, a private clinic group in Auckland, stores patient records on a central server, lets doctors access them from tablets over Wi-Fi and must keep data confidential.',
    'Nordlys Greenhouses, a farming company near Bergen, uses embedded controllers, temperature and humidity sensors and actuators to manage glasshouses, reporting to a cloud dashboard.',
    'PixelForge, a games studio in Montreal, renders 3D scenes on GPU workstations, keeps large asset files on a NAS and collaborates with freelancers around the world.',
    'Sakura Rail, a regional train operator in Osaka, runs real-time signalling on embedded systems, sells tickets online and must protect its network from attacks.',
    'Banco Andino, a savings bank in Quito, runs an online banking website, issues mobile apps to customers and encrypts all transactions.',
    'Lumen Library, a city library service in Lisbon, offers public Wi-Fi, an online catalogue and e-book lending, and runs its servers in a small on-site data room.',
    'Savanna Air, a small airline in Accra, runs its booking system on a cloud platform, uses a mesh of airport networks and processes passenger files every night.',
    'Danube Robotics, a manufacturer in Budapest, builds warehouse robots that use sensors, feedback control and on-board processors, and sends telemetry over 5G.',
]

K = Kit(R, CASE_ORGS, STYLE)


def init(subject_id):
    pass


def templates(st):
    return K.templates(st)


def pick(rng, seq, k=None):
    return rng.choice(seq) if k is None else rng.sample(seq, k)


def nmcq(rng, stem, correct, wrongs, why):
    """MCQ from numeric/text distractors: drop duplicates of the answer and return None if <3 remain."""
    ws = []
    for w in wrongs:
        w = str(w)
        if w != str(correct) and w not in ws:
            ws.append(w)
    if len(ws) < 3:
        return None
    return mcq(rng, stem, str(correct), ws[:3], why)


# =============================================================================================
# ch01 A1.1 Computer hardware and operation
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('arithmetic logic unit (ALU)', 'the part of the CPU that performs arithmetic operations and logical comparisons on data'),
           ('control unit (CU)', 'the part of the CPU that decodes instructions and sends control signals to coordinate the other components and the flow of data'),
           ('program counter (PC)', 'the register that holds the memory address of the next instruction to be fetched'),
           ('memory address register (MAR)', 'the register that holds the address of the memory location currently being read from or written to'),
           ('memory data register (MDR)', 'the register that holds the data or instruction just read from memory, or about to be written to memory'),
           ('accumulator (ACC)', 'a general-purpose register that holds the intermediate results of ALU operations'),
           ('fetch-decode-execute cycle', 'the continuous process by which the CPU fetches an instruction from memory, decodes it and carries it out'),
           ('address bus', 'the set of parallel lines that carries memory addresses from the CPU to main memory, in one direction only')],
    facts=[('During the fetch stage, which register value is copied into the MAR?', 'The program counter', ['The accumulator', 'The memory data register', 'The current instruction register'], 'MAR ← PC, so the address of the next instruction is sent along the address bus.'),
           ('Which bus is bidirectional?', 'The data bus', ['The address bus', 'Neither the data bus nor the address bus', 'Only the control bus when reading'], 'Data travel both to and from memory; addresses only travel from the CPU.'),
           ('A CPU has a 24-bit address bus and byte-addressable memory. What is the maximum memory it can address?', '16 MiB', ['24 MiB', '16 KiB', '4 GiB'], '2^24 = 16 777 216 bytes = 16 MiB.'),
           ('Which component of the CPU decides whether a branch is taken after a comparison?', 'The control unit, using the result flags set by the ALU', ['The MAR', 'The address bus', 'Main memory'], 'The ALU compares and sets flags; the CU then changes the PC if the branch is taken.'),
           ('Which register is incremented during every fetch stage?', 'Program counter', ['Memory data register', 'Accumulator', 'Memory address register'], 'PC ← PC + 1 so that it points to the next instruction.')],
    why=[('Explain why the program counter is incremented during the fetch stage rather than after execution.', 'Once the instruction has been copied into the MDR/CIR the PC is free, so incrementing it straight away prepares the address of the next instruction; if the instruction is a jump, the execute stage simply overwrites the PC with the new address.'),
         ('Explain why the MAR and MDR are both needed when the CPU reads from main memory.', 'The MAR holds the address placed on the address bus so memory knows which location to access; the MDR buffers the value returned on the data bus, so address and data are held separately while the slower memory responds.'),
         ('Explain how the control unit and the ALU work together to execute an ADD instruction.', 'The CU decodes the opcode, then signals memory to fetch the operand into the MDR and signals the ALU to add the MDR to the accumulator; the ALU performs the addition and the result is written back into the accumulator, with status flags updated.'),
         ('Explain why increasing the clock speed does not always make a program run proportionally faster.', 'Instructions may stall waiting for slower main memory or I/O, heat may force throttling, and some instructions take several cycles; so time is limited by memory access and other bottlenecks, not only by cycles per second.')],
    contrast=[('the address bus', 'the data bus', 'The address bus carries memory addresses one way (CPU to memory); the data bus carries the actual data/instructions in both directions between CPU and memory.'),
              ('the MAR', 'the MDR', 'The MAR holds the address of the memory location being accessed; the MDR holds the content (data or instruction) transferred to or from that location.'),
              ('the ALU', 'the control unit', 'The ALU performs calculations and logical comparisons; the CU decodes instructions and coordinates the components by sending control signals, but does no arithmetic itself.')],
    misc=[('The program counter counts how many instructions have been executed so far.', 'The PC holds the address of the next instruction to fetch; after a jump it can move backwards or forwards, so it is not a count.'),
          ('The MAR stores the data that is fetched from memory.', 'The MAR holds only the address; the data read from that address goes into the MDR.'),
          ('The ALU decodes instructions before carrying them out.', 'Decoding is done by the control unit; the ALU only performs the arithmetic/logic operations it is told to.')],
    evaluate=[('Adding more registers to a CPU is the most effective way to improve its performance.', ['registers are the fastest storage so fewer slow memory accesses are needed', 'compilers can keep loop variables in registers'], ['registers take die area and add complexity to instruction encoding', 'clock speed, cache size, pipelining and number of cores often have larger effects', 'context switches must save and restore more registers'], 'More registers help, but performance depends on the balance of clock speed, cache, cores and memory bandwidth; registers alone are rarely the most effective change.')],
    extended=[('A simple accumulator-based CPU executes the instruction ADD 25 (add the contents of address 25 to the accumulator). Describe, with reference to the PC, MAR, MDR, CIR, CU, ALU and the buses, how this instruction is fetched, decoded and executed.', 'Fetch: PC copied to MAR; address sent on address bus; CU sends read signal on control bus; instruction returned on data bus into MDR, copied to CIR; PC incremented. Decode: CU decodes the opcode ADD and operand 25. Execute: 25 copied to MAR; read signal; value at address 25 placed in MDR; ALU adds MDR to ACC; result stored in ACC and flags updated.', 6)],
))


def _fde_program(rng, d):
    data_base = rng.choice([20, 30, 40, 50])
    vals = [rng.randint(2, 30) for _ in range(3)]
    ops = [('LOAD', data_base), ('ADD', data_base + 1)]
    if d >= 3:
        ops.append((rng.choice(['ADD', 'SUB']), data_base + 2))
    ops.append(('STORE', data_base + 3))
    if d >= 4:
        ops += [('LOAD', data_base + 2), ('SUB', data_base)]
    ops.append(('HALT', None))
    mem = {i: f'{o} {a}' if a is not None else o for i, (o, a) in enumerate(ops)}
    for i, v in enumerate(vals):
        mem[data_base + i] = v
    return ops, mem, data_base, vals


def _fde_run(ops, mem):
    m = dict(mem)
    pc, acc, mar, mdr = 0, 0, None, None
    states = []
    while True:
        mar = pc
        mdr = m[mar]
        cir = mdr
        pc += 1
        op, a = ops[mar]
        if op == 'HALT':
            states.append(dict(PC=pc, MAR=mar, MDR=mdr, CIR=cir, ACC=acc))
            break
        mar = a
        if op == 'STORE':
            mdr = acc
            m[a] = acc
        else:
            mdr = m[a]
            acc = acc + mdr if op == 'ADD' else acc - mdr if op == 'SUB' else mdr
        states.append(dict(PC=pc, MAR=mar, MDR=mdr, CIR=cir, ACC=acc))
    return states, m


@R.add('ch01-st1', 'C3', (2, 5), 'short')
def fde_trace(rng, slot):
    ops, mem, base, vals = _fde_program(rng, slot.d)
    states, m = _fde_run(ops, mem)
    k = rng.randint(1, len(states) - 1)
    s = states[k - 1]
    listing = '\n'.join(f'{i}: {mem[i]}' for i in range(len(ops))) + '\n' + '\n'.join(f'{base + i}: {v}' for i, v in enumerate(vals))
    stem = (f'A simple CPU uses an accumulator. Main memory contains the program and data below (address: contents).\n{listing}\n'
            f'Execution starts with PC = 0 and ACC = 0. During each fetch MAR ← PC, MDR ← memory[MAR], CIR ← MDR, PC ← PC + 1; '
            f'during execute the operand address is placed in the MAR and the operand (or, for STORE, the value written) is in the MDR. '
            f'State the contents of the PC, MAR, MDR and ACC immediately after the instruction at address {k - 1} has been executed.')
    ans = f'PC = {s["PC"]}, MAR = {s["MAR"]}, MDR = {s["MDR"]}, ACC = {s["ACC"]}'
    return dict(stem=stem, answer=ans, markingKey=f'1 mark each: {ans}. (Trace: ' + '; '.join(f'after {i}: ACC={st["ACC"]}' for i, st in enumerate(states[:k])) + ')', marks=4)


@R.add('ch01-st1', 'C3', (2, 5), 'numerical')
def fde_final(rng, slot):
    ops, mem, base, vals = _fde_program(rng, max(3, slot.d))
    states, m = _fde_run(ops, mem)
    listing = '\n'.join(f'{i}: {mem[i]}' for i in range(len(ops))) + '\n' + '\n'.join(f'{base + i}: {v}' for i, v in enumerate(vals))
    who = pick(rng, PEOPLE)
    stem = (f'{who} hand-traces this accumulator program (address: contents) starting with ACC = 0.\n{listing}\n'
            f'State the value stored at address {base + 3} and the value in the accumulator when the program halts, and the number of fetch-decode-execute cycles completed.')
    ans = f'Address {base + 3} = {m[base + 3]}; ACC = {states[-1]["ACC"]}; {len(states)} cycles (including HALT)'
    return dict(stem=stem, answer=ans, markingKey=f'{ans}. 1 mark for each value.', marks=3)


@R.add('ch01-st1', 'C3', (1, 4), 'numerical')
def clock_time(rng, slot):
    n = rng.choice([2, 5, 8, 12, 40]) * 10 ** rng.choice([6, 7, 8])
    cpi = rng.choice([1, 1.5, 2, 2.5, 4])
    f = rng.choice([1.2, 2, 2.5, 3, 3.6, 4])
    t = n * cpi / (f * 1e9)
    frame = rng.choice(['A benchmark program', 'An image-filter routine', 'A sorting job', 'A video-encoding step'])
    stem = f'{frame} executes {n:,} instructions with an average of {cpi} clock cycles per instruction on a {f} GHz single-core CPU. Calculate the execution time in milliseconds.'
    ans = f'{r2(t * 1000, 3)} ms'
    return dict(stem=stem, answer=ans, markingKey=f'Cycles = {n:,} × {cpi} = {n * cpi:,.0f} (M1); time = cycles ÷ {f}×10^9 Hz (M1) = {r2(t * 1000, 3)} ms (A1).', marks=3)


@R.add('ch01-st1', 'C1', (1, 3), 'mcq')
def bus_mcq(rng, slot):
    n = rng.choice([8, 10, 12, 16, 20, 24, 32])
    v = 2 ** n
    def h(x):
        for u, s in ((2 ** 30, 'GiB'), (2 ** 20, 'MiB'), (2 ** 10, 'KiB')):
            if x >= u:
                return f'{r2(x / u)} {s}'
        return f'{x} bytes'
    return nmcq(rng, f'A processor has a {n}-bit address bus and each address refers to one byte. What is the maximum amount of memory it can address?',
                h(v), [h(2 ** (n - 1)), h(2 ** (n + 1)), f'{n} bytes', h(n * 1024), h(2 ** (n + 2))], f'2^{n} addresses × 1 byte = {h(v)}.')


K.ar('ch01-st1', [
    ('The MAR is connected to the address bus.', 'The MAR holds the address of the memory location to be accessed.', 0, 'Both true; holding the address is why the MAR drives the address bus.'),
    ('The data bus is bidirectional.', 'The address bus carries addresses only from the CPU to memory.', 1, 'Both true, but the one-way address bus does not explain why the data bus is two-way (data must be both read and written).'),
    ('A jump instruction changes the program counter during the execute stage.', 'The program counter holds the address of the next instruction to be fetched.', 0, 'Both true; because the PC determines the next fetch, overwriting it makes the jump happen.'),
    ('The ALU contains the program counter.', 'The ALU performs arithmetic and logical operations.', 3, 'A is false (PC is a separate register controlled by the CU); R is true.'),
])


R.facts('ch01-st2', F(
    terms=[('graphics processing unit (GPU)', 'a processor with thousands of simple cores designed to perform the same operation on many data items in parallel, originally for rendering images'),
           ('parallel processing', 'carrying out many calculations at the same time on multiple cores or processing units'),
           ('SIMD (single instruction, multiple data)', 'a form of parallelism in which one instruction is applied to many data items at once'),
           ('throughput', 'the amount of work completed per unit of time, such as pixels rendered or operations per second'),
           ('latency', 'the time taken to complete a single task or respond to a single request'),
           ('multi-core processor', 'a single chip containing two or more independent processing cores that can execute instructions simultaneously')],
    facts=[('Which task is best suited to a GPU rather than a CPU?', 'Applying the same brightness filter to every pixel of a 4K video frame', ['Running the operating system scheduler', 'Processing a single complex branching tax calculation', 'Handling keyboard interrupts'], 'Identical, independent operations on millions of pixels suit massively parallel SIMD cores.'),
           ('Compared with a CPU core, a typical GPU core is…', 'simpler, with less control logic and cache, but there are many more of them', ['more complex, with larger caches', 'faster at executing a single sequential thread', 'designed mainly for branch prediction'], 'GPUs trade per-core sophistication for very high core counts.'),
           ('Why are GPUs widely used to train neural networks?', 'Training is dominated by large matrix multiplications that can be split across many cores', ['Neural networks require high single-thread clock speeds', 'GPUs have more secondary storage', 'GPUs do not need main memory'], 'Matrix operations are data-parallel.'),
           ('Which statement about CPUs is correct?', 'CPUs are optimised for low latency on varied, sequential and branching tasks', ['CPUs always have more cores than GPUs', 'CPUs cannot run in parallel', 'CPUs are used only for graphics'], 'Large caches and branch prediction make CPUs good at general-purpose sequential work.')],
    why=[('Explain why a GPU can render a 3D scene much faster than a CPU even though each GPU core has a lower clock speed.', 'Rendering applies the same calculations to millions of independent pixels/vertices; the GPU has thousands of cores working simultaneously, so total throughput is far higher even though each core is slower.'),
         ('Explain why not every program runs faster on a GPU.', 'Programs with sequential steps, many branches or data dependencies cannot be split into independent parallel tasks, and copying data to and from GPU memory adds overhead, so the CPU may be faster.'),
         ('Explain why CPUs devote much of their chip area to cache and control logic.', 'General-purpose code is sequential and branch-heavy, so large caches reduce memory latency and branch prediction/out-of-order logic keep a single thread running quickly.'),
         ('Explain why the speed-up from adding more cores eventually levels off (Amdahl\'s law).', 'Only the parallel part of a program benefits from more cores; the sequential part still runs on one core, so as the number of cores grows the run time approaches the sequential time and speed-up is limited to 1/(1 − p).')],
    contrast=[('a CPU', 'a GPU', 'A CPU has a few powerful cores with large caches and complex control, optimised for low-latency sequential and branching tasks; a GPU has thousands of simple cores optimised for high-throughput parallel processing of similar data.'),
              ('latency', 'throughput', 'Latency is the time for one task to complete; throughput is the number of tasks completed per unit time. CPUs minimise latency, GPUs maximise throughput.')],
    misc=[('A GPU is just a faster CPU, so it could replace the CPU in a laptop.', 'GPU cores are simpler and slow at sequential, branching work such as running the OS; the CPU is still needed to control the system and run general code.'),
          ('Doubling the number of cores always halves the run time of a program.', 'Only the parallelisable part speeds up and there is overhead for coordination, so the improvement is less than double (Amdahl\'s law).'),
          ('GPUs are only useful for video games.', 'GPUs are widely used for machine learning, scientific simulation, video encoding and cryptocurrency mining because these are data-parallel tasks.')],
    evaluate=[('A school should buy GPU workstations rather than CPU-only computers for its computer science lab.', ['GPUs accelerate machine-learning projects, rendering and simulations', 'students gain experience with parallel programming'], ['most programming tasks are sequential and run well on a CPU', 'GPU workstations cost more and use more power', 'software may need special frameworks (CUDA) to use the GPU'], 'Only worthwhile if the curriculum includes ML, graphics or simulation; otherwise CPU computers give better value.')],
    extended=[('A weather service runs a simulation in which 92% of the work can be parallelised. Compare running it on an 8-core CPU and on a GPU with 2048 cores, using Amdahl\'s law, and discuss two other factors that affect which processor is better.', 'Speed-up = 1/((1 − p) + p/N): 8 cores → 1/(0.08 + 0.115) ≈ 5.13; 2048 cores → 1/(0.08 + 0.000449) ≈ 12.43, limited by the 8% serial part (max 12.5). Other factors: cost of copying data to GPU memory, whether the code can be written for the GPU, power consumption, memory size; the GPU gives about 2.4× more speed-up but serial code dominates.', 6)],
))


@R.add('ch01-st2', 'C3', (2, 5), 'numerical')
def amdahl(rng, slot):
    p = rng.choice([0.5, 0.6, 0.75, 0.8, 0.9, 0.95, 0.99])
    n = rng.choice([2, 4, 8, 16, 64, 256, 1024])
    s = 1 / ((1 - p) + p / n)
    ctx = rng.choice(['a video-encoding job', 'a physics simulation', 'a password-hashing benchmark', 'an image-classification batch', 'a protein-folding calculation'])
    stem = f'{int(p * 100)}% of {ctx} can be run in parallel. Using Amdahl\'s law, calculate the speed-up when it runs on {n} cores'
    ans = f'{r2(s)}×'
    key = f'Speed-up = 1 / ((1 − {p}) + {p}/{n}) (M1) = {r2(s)} (A1).'
    if slot.d >= 4:
        stem += ', and state the maximum possible speed-up with unlimited cores'
        ans += f'; maximum = 1/(1 − {p}) = {r2(1 / (1 - p))}×'
        key += f' Limit as N → ∞: 1/{r2(1 - p)} = {r2(1 / (1 - p))} (A1).'
    return dict(stem=stem + '.', answer=ans, markingKey=key, marks=3 if slot.d >= 4 else 2)


@R.add('ch01-st2', 'C3', (2, 5), 'numerical')
def gpu_time(rng, slot):
    w, h = pick(rng, [(1920, 1080), (3840, 2160), (2560, 1440), (1280, 720)])
    ops = rng.choice([50, 100, 200, 400])
    cpu_c, cpu_r = rng.choice([4, 8, 16]), rng.choice([2, 4])        # cores, Gop/s per core
    gpu_c, gpu_r = rng.choice([1024, 2048, 4096]), rng.choice([0.5, 1])
    total = w * h * ops
    tc = total / (cpu_c * cpu_r * 1e9)
    tg = total / (gpu_c * gpu_r * 1e9)
    stem = (f'A filter needs {ops} operations per pixel on a {w}×{h} frame. A CPU has {cpu_c} cores each doing {cpu_r} × 10^9 operations per second; '
            f'a GPU has {gpu_c} cores each doing {gpu_r} × 10^9 operations per second. Assuming perfect parallelism, calculate the time per frame on each '
            f'and how many times faster the GPU is.')
    ans = f'CPU {r2(tc * 1000, 3)} ms, GPU {r2(tg * 1000, 3)} ms; GPU ≈ {r2(tc / tg)}× faster'
    return dict(stem=stem, answer=ans, markingKey=f'Total ops = {w}×{h}×{ops} = {total:,} (M1); CPU = total/({cpu_c}×{cpu_r}e9) = {r2(tc * 1000, 3)} ms (A1); GPU = total/({gpu_c}×{gpu_r}e9) = {r2(tg * 1000, 3)} ms (A1); ratio {r2(tc / tg)} (A1).', marks=4)


_PROC_TASKS = [('training a convolutional neural network on 50 000 images', 'GPU', 'the work is large matrix multiplications that are data-parallel'),
               ('running a word processor and spell-checker', 'CPU', 'the work is sequential, interactive and branch-heavy'),
               ('rendering frames for a 3D animated film', 'GPU', 'each pixel/vertex can be shaded independently in parallel'),
               ('compiling a large Java project', 'CPU', 'compilation involves complex, branching, mostly sequential work'),
               ('mining a proof-of-work cryptocurrency', 'GPU', 'billions of independent hash attempts can run in parallel'),
               ('handling interrupts and scheduling processes in the OS', 'CPU', 'it requires low latency, complex control and privileged instructions'),
               ('encoding a 4K video', 'GPU', 'blocks of pixels can be transformed in parallel (dedicated GPU encoders)'),
               ('querying a small database with complex joins', 'CPU', 'the task is latency-sensitive with irregular memory access and branching'),
               ('simulating fluid flow on a grid of 10 million cells', 'GPU', 'the same update is applied to every cell each time step')]


@R.add('ch01-st2', 'C3', (1, 4), 'short')
def cpu_or_gpu(rng, slot):
    k = 2 if slot.d <= 2 else 3
    ts = rng.sample(_PROC_TASKS, k)
    lst = '; '.join(f'({chr(97 + i)}) {t[0]}' for i, t in enumerate(ts))
    ans = '; '.join(f'({chr(97 + i)}) {t[1]} – {t[2]}' for i, t in enumerate(ts))
    return dict(stem=f'For each task, state whether a CPU or a GPU is more suitable and justify your choice: {lst}.', answer=ans,
                markingKey=f'1 mark per correct choice with justification: {ans}.', marks=k)


K.ar('ch01-st2', [
    ('GPUs achieve high throughput on image processing.', 'GPUs contain thousands of simple cores that apply the same instruction to many pixels at once.', 0, 'Both true; SIMD parallelism is the reason.'),
    ('Adding cores cannot speed up a program beyond 1/(1 − p).', 'The sequential fraction (1 − p) of a program must still run on one core.', 0, 'Both true; the serial part bounds the speed-up.'),
    ('CPUs are better than GPUs at running the operating system.', 'CPUs have more cores than GPUs.', 2, 'A true; R false (GPUs have far more cores).'),
    ('A GPU is a type of secondary storage.', 'GPUs have their own dedicated video memory (VRAM).', 3, 'A false (a GPU is a processor); R true.'),
    ('Training deep neural networks is usually done on GPUs.', 'GPUs have higher clock speeds than CPUs.', 2, 'A true; R false – GPU cores are usually clocked lower; the benefit is parallelism.'),
])


R.facts('ch01-st3', F(
    terms=[('RAM (random-access memory)', 'volatile main memory that holds the programs and data currently in use and can be read from and written to'),
           ('ROM (read-only memory)', 'non-volatile memory whose contents are fixed (or rarely changed) and which typically holds the firmware/bootstrap program'),
           ('cache memory', 'a small amount of very fast memory close to or inside the CPU that stores copies of frequently used instructions and data'),
           ('volatile memory', 'memory that loses its contents when the power is switched off'),
           ('cache hit', 'an access in which the requested data is found in the cache, so slower main memory need not be accessed'),
           ('virtual memory', 'part of secondary storage used as an extension of RAM when RAM is full, with pages swapped in and out'),
           ('memory hierarchy', 'the arrangement of storage from small, fast, expensive registers and cache down to large, slow, cheap secondary storage')],
    facts=[('Which type of memory stores the BIOS/UEFI start-up instructions?', 'ROM (flash firmware)', ['RAM', 'L1 cache', 'Virtual memory'], 'Firmware must survive power-off, so it is held in non-volatile ROM/flash.'),
           ('Which order lists memory from fastest to slowest?', 'Registers, L1 cache, L2 cache, RAM, SSD', ['RAM, cache, registers, SSD', 'SSD, RAM, cache, registers', 'L2 cache, registers, RAM, L1 cache'], 'Speed falls (and capacity rises) moving away from the CPU.'),
           ('Why does cache improve performance?', 'Programs repeatedly access the same or nearby data (locality), which can be served from fast cache', ['Cache is larger than RAM', 'Cache is non-volatile', 'Cache replaces the need for registers'], 'Temporal and spatial locality give high hit rates.'),
           ('What happens when RAM is full and virtual memory is used heavily?', 'Thrashing: the computer slows down because pages are constantly swapped with the disk', ['The CPU clock speed increases', 'ROM is used to store programs', 'The cache becomes non-volatile'], 'Disk access is thousands of times slower than RAM.')],
    why=[('Explain why main memory is volatile but this is acceptable.', 'RAM uses circuits (DRAM capacitors) that need power to hold data; this makes it fast and cheap per bit, and anything that must persist is saved to non-volatile secondary storage.'),
         ('Explain why a computer has several levels of cache rather than a single large cache.', 'Small caches can be very fast and close to the core (L1), while larger caches (L2/L3) are slower but hold more; the hierarchy balances speed, cost and hit rate.'),
         ('Explain why increasing RAM can make a computer faster even if the CPU is unchanged.', 'With more RAM, more programs and data fit in main memory, so less virtual memory paging to slow disk is needed and thrashing is avoided.'),
         ('Explain the role of locality of reference in cache design.', 'Programs tend to reuse recently accessed data (temporal locality) and data stored nearby (spatial locality), so the cache keeps recent items and loads whole blocks, giving a high hit rate.')],
    contrast=[('RAM', 'ROM', 'RAM is volatile, read-write and holds the currently running programs and data; ROM is non-volatile, normally read-only and holds firmware such as the boot program.'),
              ('cache', 'virtual memory', 'Cache is small, very fast memory between CPU and RAM that speeds up access; virtual memory uses slow secondary storage to extend RAM when it is full.'),
              ('SRAM', 'DRAM', 'SRAM uses flip-flops, is faster, more expensive and used for cache; DRAM stores bits in capacitors that must be refreshed, is cheaper and denser and used for main memory.')],
    misc=[('Cache memory is a type of secondary storage that keeps files after the power is off.', 'Cache is volatile primary memory inside or near the CPU; it holds copies of data in use, not files.'),
          ('More cache always means a faster computer.', 'Larger caches have longer access times and diminishing returns once the working set fits; performance also depends on clock speed and cores.'),
          ('ROM cannot be changed at all, so firmware updates are impossible.', 'Modern ROM is flash/EEPROM which can be rewritten (flashed) occasionally, which is how firmware updates are installed.')],
    evaluate=[('Upgrading RAM is the most cost-effective way to speed up an old laptop.', ['eliminates paging/thrashing if RAM is the bottleneck', 'cheap compared with a new CPU'], ['no effect if RAM is not full', 'an SSD may give a bigger improvement for boot and load times', 'some laptops have soldered RAM'], 'Only when the laptop regularly runs out of RAM; otherwise replacing a hard disk with an SSD is usually more effective.')],
    extended=[('A CPU has a cache with access time 2 ns and main memory with access time 60 ns. Explain, with a calculation for a hit rate of 95%, why caches dramatically reduce the average memory access time, and discuss why the hit rate can fall.', 'Average = 0.95 × 2 + 0.05 × (2 + 60) = 1.9 + 3.1 = 5 ns compared with 60 ns without cache: 12× faster. The hit rate falls when the working set is larger than the cache, when access patterns have poor locality (random access), or after context switches flush useful data.', 6)],
))


@R.add('ch01-st3', 'C3', (2, 5), 'numerical')
def cache_eat(rng, slot):
    tc = rng.choice([1, 2, 3, 5])
    tm = rng.choice([50, 60, 80, 100, 120])
    h = rng.choice([80, 85, 90, 95, 97, 98, 99])
    model = rng.choice(['seq', 'par'])
    if model == 'seq':
        t = h / 100 * tc + (1 - h / 100) * (tc + tm)
        rule = 'on a miss the cache is checked first and then main memory is accessed'
        work = f'{h / 100} × {tc} + {r2(1 - h / 100)} × ({tc} + {tm})'
    else:
        t = h / 100 * tc + (1 - h / 100) * tm
        rule = 'cache and main memory are searched at the same time, so a miss costs only the main-memory time'
        work = f'{h / 100} × {tc} + {r2(1 - h / 100)} × {tm}'
    stem = f'A cache has an access time of {tc} ns and main memory {tm} ns; the hit rate is {h}%. Assume {rule}. Calculate the effective (average) memory access time.'
    ans = f'{r2(t)} ns'
    return dict(stem=stem, answer=ans, markingKey=f'{work} (M1) = {r2(t)} ns (A1). Without cache: {tm} ns, so ≈ {r2(tm / t)}× faster.', marks=2 if slot.d <= 3 else 3)


def _lru(seq, size):
    cache, hits, log = [], 0, []
    for x in seq:
        if x in cache:
            hits += 1
            cache.remove(x)
            cache.append(x)
            log.append('H')
        else:
            if len(cache) == size:
                cache.pop(0)
            cache.append(x)
            log.append('M')
    return hits, cache, log


def _fifo(seq, size):
    cache, hits, log = [], 0, []
    for x in seq:
        if x in cache:
            hits += 1
            log.append('H')
        else:
            if len(cache) == size:
                cache.pop(0)
            cache.append(x)
            log.append('M')
    return hits, cache, log


@R.add('ch01-st3', 'C3', (2, 5), 'short')
def cache_sim(rng, slot):
    size = 3 if slot.d <= 3 else rng.choice([3, 4])
    blocks = rng.sample('ABCDEFGH', size + 2)
    seq = [rng.choice(blocks[:size + 1]) if rng.random() < 0.7 else rng.choice(blocks) for _ in range(8 + slot.d)]
    pol = rng.choice(['LRU', 'FIFO'])
    hits, cache, log = (_lru if pol == 'LRU' else _fifo)(seq, size)
    stem = (f'A cache holds {size} blocks and is initially empty. It uses {pol} replacement '
            f'({"least recently used block is evicted" if pol == "LRU" else "the block that has been in the cache longest is evicted"}). '
            f'The CPU requests these blocks in order: {" ".join(seq)}. State the number of hits and misses, the hit rate, and the final contents of the cache.')
    ans = f'{hits} hits, {len(seq) - hits} misses, hit rate {r2(100 * hits / len(seq), 1)}%; final cache {{{", ".join(sorted(cache))}}}'
    return dict(stem=stem, answer=ans, markingKey=f'Sequence of results: {" ".join(log)}. {ans}. 1 mark each for hits/misses, hit rate and final contents; 1 mark for a correct trace.', marks=4)


@R.add('ch01-st3', 'C1', (1, 3), 'mcq')
def mem_where(rng, slot):
    items = [('the bootstrap loader that runs when the computer is switched on', 'ROM'),
             ('the document a user is currently editing', 'RAM'),
             ('the instructions inside a loop that is executing repeatedly', 'Cache'),
             ('pages of a program swapped out because RAM is full', 'Virtual memory on secondary storage'),
             ('the result of the most recent ALU operation', 'A register (accumulator)'),
             ('the operating system kernel while the computer is running', 'RAM')]
    what, ans = rng.choice(items)
    others = ['ROM', 'RAM', 'Cache', 'Virtual memory on secondary storage', 'A register (accumulator)']
    return nmcq(rng, f'Where is {what} most likely to be held?', ans, rng.sample([o for o in others if o != ans], 3), f'{ans} is the correct level of the memory hierarchy for {what}.')


K.ar('ch01-st3', [
    ('Cache memory reduces the average time for the CPU to access data.', 'Cache stores frequently used data in faster memory close to the CPU.', 0, 'Both true; R is why.'),
    ('RAM is non-volatile.', 'RAM is used to hold programs that are currently running.', 3, 'A false (RAM is volatile); R true.'),
    ('Heavy use of virtual memory slows a computer down.', 'Secondary storage is much slower to access than RAM.', 0, 'Both true; slow disk access causes the slowdown.'),
    ('ROM holds the firmware needed to start the computer.', 'ROM is faster than cache.', 2, 'A true; R false – cache is far faster than ROM.'),
])


R.facts('ch01-st4', F(
    terms=[('secondary storage', 'non-volatile storage that keeps programs and data permanently, such as HDDs, SSDs, optical discs and flash drives'),
           ('solid-state drive (SSD)', 'secondary storage that uses NAND flash memory with no moving parts'),
           ('hard disk drive (HDD)', 'magnetic secondary storage in which a read/write head moves over spinning platters'),
           ('lossless compression', 'compression that reduces file size so that the original data can be reconstructed exactly, e.g. run-length encoding'),
           ('lossy compression', 'compression that permanently removes data judged less important, so the original cannot be reconstructed exactly, e.g. JPEG or MP3'),
           ('run-length encoding (RLE)', 'a lossless method that replaces a run of repeated values with a single value and a count'),
           ('compression ratio', 'original size divided by compressed size')],
    facts=[('Which compression method is suitable for a program\'s executable file?', 'Lossless', ['Lossy', 'Either – it makes no difference', 'Neither – programs cannot be compressed'], 'Every bit of a program must be restored exactly or it will not run.'),
           ('Which storage device has the fastest random access time?', 'SSD', ['HDD', 'Magnetic tape', 'Blu-ray disc'], 'No moving parts, so no seek or rotational delay.'),
           ('Which storage medium is most cost-effective for long-term archive backups of petabytes of data?', 'Magnetic tape', ['SSD', 'RAM', 'USB flash drive'], 'Tape has the lowest cost per gigabyte and is durable for archives, though access is sequential.'),
           ('Which file format uses lossy compression?', 'MP3', ['PNG', 'ZIP', 'FLAC'], 'MP3 discards sounds that humans hear poorly.')],
    why=[('Explain why an SSD is faster than an HDD for loading many small files.', 'An HDD must move its head and wait for the platter to rotate for each file (seek + rotational latency), while an SSD accesses any block electronically in roughly constant time.'),
         ('Explain why lossy compression is acceptable for photographs shared on social media.', 'Small losses of detail are barely noticeable to the human eye, and the much smaller files load faster and use less bandwidth and storage.'),
         ('Explain why run-length encoding can make some files larger.', 'If data rarely repeats, each single value is replaced by a value and a count, so the encoded data can be up to twice as large.'),
         ('Explain why SSDs wear out over time.', 'Each flash cell can only be written/erased a limited number of times; wear-levelling spreads writes, but cells eventually fail.')],
    contrast=[('lossless compression', 'lossy compression', 'Lossless compression allows the exact original to be restored (used for text, programs); lossy compression permanently discards some data for much smaller files (used for images, audio, video).'),
              ('an SSD', 'an HDD', 'An SSD uses flash memory with no moving parts – faster, more robust, lower power but more expensive per GB; an HDD uses spinning magnetic platters – cheaper per GB and larger capacity but slower and fragile.')],
    misc=[('Compressing a file with RLE twice makes it half the size again.', 'After the first pass the runs have been removed; encoding again usually makes the file bigger, not smaller.'),
          ('A ZIP file is lossy because it makes the file smaller.', 'ZIP uses lossless compression; size reduction alone does not imply data loss.'),
          ('SSDs store data magnetically, which is why they are faster.', 'SSDs store charge in flash memory cells; they are faster because there are no moving parts.')],
    evaluate=[('Cloud storage has made local secondary storage unnecessary.', ['access from anywhere and automatic backup', 'scalable without buying hardware'], ['needs a fast, reliable internet connection', 'ongoing subscription costs and privacy concerns', 'the OS and applications still need local storage for speed'], 'Cloud storage complements but does not replace local storage, which is still needed for the OS, speed and offline use.')],
    extended=[('A photographer in Cape Town must store 2 TB of RAW photos, edit current projects quickly and keep an off-site backup. Recommend a combination of storage devices and compression methods, justifying each choice.', 'SSD (e.g. 1 TB NVMe) for current projects – fast loading of large files; large HDD (4 TB) for the full library – cheap per GB; cloud or tape for off-site backup. RAW files stored losslessly to keep full quality; JPEG (lossy) exports for sharing online because smaller; ZIP/lossless for archives. Justifications must link speed, capacity, cost and data loss.', 6)],
))


def _rle(s):
    out = []
    for ch, g in itertools.groupby(s):
        out.append(f'{len(list(g))}{ch}')
    return ''.join(out)


@R.add('ch01-st4', 'C3', (1, 4), 'short')
def rle_encode(rng, slot):
    n = 3 + slot.d
    sym = rng.sample('WBRGY', 2 if slot.d <= 2 else 3)
    s = ''.join(rng.choice(sym) * rng.randint(1, 6) for _ in range(n))
    enc = _rle(s)
    mode = rng.choice(['enc', 'dec']) if slot.d >= 3 else 'enc'
    if mode == 'enc':
        stem = f'A row of pixels in a simple image is stored as the characters {s} ({len(s)} characters). Encode it using run-length encoding in the form count followed by colour (e.g. 3W), and state how many characters the encoded form uses.'
        ans = f'{enc} ({len(enc)} characters)'
    else:
        stem = f'A row of pixels has been run-length encoded as {enc} (count followed by colour). Decode it and state the number of pixels in the row.'
        ans = f'{s} ({len(s)} pixels)'
    return dict(stem=stem, answer=ans, markingKey=f'{ans}. 1 mark per correct run group (max 2), 1 mark for the count.', marks=3)


@R.add('ch01-st4', 'C3', (2, 5), 'numerical')
def comp_ratio(rng, slot):
    w, h = pick(rng, [(1920, 1080), (1280, 720), (4000, 3000), (800, 600)])
    bits = rng.choice([24, 32])
    ratio = rng.choice([4, 5, 8, 10, 12])
    raw = w * h * bits / 8
    comp = raw / ratio
    bw = rng.choice([8, 20, 50, 100])  # Mbit/s
    t1, t2 = raw * 8 / (bw * 1e6), comp * 8 / (bw * 1e6)
    stem = (f'A {w}×{h} image uses {bits}-bit colour. It is compressed with a lossy method at a compression ratio of {ratio}:1 and sent over a {bw} Mbit/s link. '
            f'Calculate the uncompressed and compressed sizes in MB (1 MB = 10^6 bytes) and the time saved in sending the compressed version.')
    ans = f'{r2(raw / 1e6)} MB uncompressed, {r2(comp / 1e6)} MB compressed; time saved {r2(t1 - t2)} s'
    return dict(stem=stem, answer=ans, markingKey=f'Raw = {w}×{h}×{bits}/8 = {raw:,.0f} B (M1 A1); ÷{ratio} = {comp:,.0f} B (A1); times {r2(t1)} s and {r2(t2)} s, saved {r2(t1 - t2)} s (A1).', marks=4)


@R.add('ch01-st4', 'C3', (1, 4), 'short')
def storage_choice(rng, slot):
    items = [('a hospital archiving 15 years of scans that are rarely read', 'magnetic tape or cloud cold storage', 'very large capacity at the lowest cost per GB; slow sequential access is acceptable for rarely used data'),
             ('a laptop that must boot quickly and survive being dropped', 'SSD', 'fast access with no moving parts, so robust and quick to boot'),
             ('a CCTV recorder that writes video continuously and needs 8 TB', 'HDD', 'cheap high capacity and handles continuous sequential writes'),
             ('a student moving coursework between school and home', 'USB flash drive or cloud storage', 'portable, small and robust; cloud gives access from anywhere'),
             ('a music producer distributing a limited physical album', 'optical disc (CD)', 'cheap to mass-produce and widely playable'),
             ('a games console that must load large levels quickly', 'NVMe SSD', 'very high read speeds reduce loading times')]
    who, dev, why = rng.choice(items)
    return dict(stem=f'Recommend a suitable secondary storage device for {who}. Justify your choice with two characteristics of the device.', answer=f'{dev}: {why}.',
                markingKey=f'1 mark for a suitable device ({dev}); 1 mark each for two justified characteristics: {why}.', marks=3)


K.ar('ch01-st4', [
    ('PNG images can be restored exactly after decompression.', 'PNG uses lossless compression.', 0, 'Both true; lossless compression is why.'),
    ('Run-length encoding is lossy.', 'Run-length encoding replaces runs of repeated values with a count and the value.', 3, 'A false (RLE is lossless); R true.'),
    ('SSDs have faster access times than HDDs.', 'SSDs have no moving read/write heads.', 0, 'Both true; no seek time is why.'),
    ('Lossy compression is suitable for bank transaction files.', 'Lossy compression gives smaller files than lossless.', 3, 'A false – any lost data would corrupt the records; R true.'),
])


R.facts('ch01-st5', F(
    terms=[('cloud computing', 'the delivery of computing resources such as storage, processing and software over the internet on demand, usually paid for as used'),
           ('SaaS (software as a service)', 'a cloud model in which complete applications are provided over the internet and managed entirely by the provider, e.g. web email'),
           ('PaaS (platform as a service)', 'a cloud model providing a managed platform (runtime, database, tools) on which customers develop and deploy their own applications'),
           ('IaaS (infrastructure as a service)', 'a cloud model providing virtual machines, storage and networks that the customer configures and manages, including the operating system'),
           ('scalability', 'the ability to increase or decrease computing resources quickly to match demand'),
           ('virtualisation', 'running several virtual machines, each with its own OS, on one physical server')],
    facts=[('A start-up rents virtual servers, installs its own Linux and database, and manages patches itself. Which model is this?', 'IaaS', ['SaaS', 'PaaS', 'On-premises'], 'The customer manages the OS upwards; the provider supplies infrastructure.'),
           ('A school uses an online office suite through a browser. Which cloud model is this?', 'SaaS', ['IaaS', 'PaaS', 'Hybrid IaaS'], 'The complete application is provided and managed by the vendor.'),
           ('Developers upload their code to a service that automatically handles the runtime, scaling and OS. Which model is this?', 'PaaS', ['SaaS', 'IaaS', 'Peer-to-peer'], 'The platform is managed; the customer manages only the application and data.'),
           ('Which is a disadvantage of cloud computing for a business?', 'Dependence on internet connectivity and the provider', ['No need to buy servers', 'Pay only for what is used', 'Easy to scale'], 'If the connection or provider fails, services are unavailable.')],
    why=[('Explain why cloud computing suits a business with highly variable demand, such as a ticket-selling website.', 'Resources can be scaled up automatically for peaks (e.g. a concert release) and scaled down afterwards, so the business pays only for what it uses instead of buying servers for the peak.'),
         ('Explain why a company might choose IaaS instead of SaaS.', 'IaaS gives full control over the OS, software and configuration, so the company can run custom or legacy software and meet specific security settings, although it must manage and patch them itself.'),
         ('Explain why storing data in the cloud raises legal concerns for a European hospital.', 'Data may be stored in data centres in other countries with different laws; GDPR requires control over where personal data is processed and how it is protected, so the hospital must ensure the provider complies.')],
    contrast=[('SaaS', 'IaaS', 'In SaaS the provider manages everything and the customer just uses the application; in IaaS the provider supplies virtual hardware and the customer manages the OS, middleware, applications and data.'),
              ('PaaS', 'IaaS', 'PaaS provides a managed runtime and tools so the customer only deploys code and data; IaaS provides raw virtual machines so the customer also manages the OS and runtime.'),
              ('public cloud', 'private cloud', 'A public cloud shares a provider\'s infrastructure among many customers over the internet; a private cloud is dedicated to one organisation, giving more control and security at higher cost.')],
    misc=[('With SaaS the customer must install and update the software on each computer.', 'In SaaS the provider runs and updates the software; users access it through a browser or thin client.'),
          ('Cloud computing means data is not stored on any physical computer.', 'Cloud data is stored on physical servers in the provider\'s data centres; the user simply does not manage them.'),
          ('Moving to the cloud always reduces costs.', 'Steady, heavy workloads can cost more in the cloud over time; savings depend on usage patterns and on avoided staff and hardware costs.')],
    evaluate=[('A small school should move all its IT services to the cloud.', ['no servers to buy or maintain; automatic backups and updates', 'access from home for staff and students'], ['dependence on internet reliability and bandwidth', 'subscription costs continue every year', 'data protection concerns about student records'], 'Moving most services (email, documents) to SaaS is sensible, but the school needs a reliable connection and should check data-protection terms.')],
    extended=[('A small online shop in Kuala Lumpur currently hosts its website on one server in its office. Discuss whether it should move to IaaS, PaaS or SaaS (an e-commerce platform), considering cost, control, scalability and the skills of its two staff.', 'SaaS e-commerce platform: least technical skill, provider handles security and scaling, monthly fee, limited customisation. PaaS: deploy own code without managing OS, good scaling, needs developer skills. IaaS: most control but staff must manage OS, patches and security. With two non-specialist staff, SaaS (or PaaS if custom features are essential) is most appropriate; on-site server has single point of failure and poor scalability.', 6)],
))

_CLOUD_LAYERS = ['applications', 'data', 'runtime', 'middleware', 'operating system', 'virtualisation', 'servers', 'storage', 'networking']
_CLOUD_SPLIT = {'IaaS': 5, 'PaaS': 2, 'SaaS': 0, 'on-premises': 9}


@R.add('ch01-st5', 'C3', (1, 4), 'short')
def cloud_resp(rng, slot):
    model = rng.choice(['IaaS', 'PaaS', 'SaaS'])
    layers = rng.sample(_CLOUD_LAYERS, 4)
    cust = set(_CLOUD_LAYERS[:_CLOUD_SPLIT[model]])
    res = [f'{l}: {"customer" if l in cust else "provider"}' for l in layers]
    return dict(stem=f'A company uses {model}. For each of the following layers state whether the customer or the cloud provider is responsible for managing it: {", ".join(layers)}.',
                answer='; '.join(res), markingKey='1 mark per correct layer: ' + '; '.join(res) + f'. (In {model} the customer manages: {", ".join(_CLOUD_LAYERS[:_CLOUD_SPLIT[model]]) or "nothing except user settings"}.)', marks=4)


@R.add('ch01-st5', 'C3', (2, 5), 'numerical')
def cloud_cost(rng, slot):
    server = rng.choice([6000, 8000, 12000, 15000])
    maint = rng.choice([150, 200, 300, 400])
    rate = rng.choice([0.12, 0.2, 0.35, 0.5])
    hours = rng.choice([200, 300, 450, 720])
    months = rng.choice([12, 24, 36])
    cloud_m = rate * hours
    onp = server + maint * months
    cl = cloud_m * months
    be = server / (cloud_m - maint) if cloud_m > maint else None
    stem = (f'A firm compares buying a server for ${server:,} plus ${maint} per month maintenance with renting a cloud VM at ${rate} per hour for about {hours} hours per month. '
            f'Calculate the total cost of each option over {months} months and state which is cheaper.' + (' Determine after how many months the costs are equal.' if slot.d >= 4 and be else ''))
    ans = f'On-premises ${onp:,.0f}; cloud ${cl:,.2f}; {"cloud" if cl < onp else "on-premises"} is cheaper'
    key = f'On-prem = {server} + {maint}×{months} = {onp:,.0f} (M1 A1); cloud = {rate}×{hours}×{months} = {cl:,.2f} (M1 A1).'
    if slot.d >= 4 and be:
        ans += f'; break-even ≈ {r2(be, 1)} months'
        key += f' Break-even: {server} = ({r2(cloud_m)} − {maint})·m → m = {r2(be, 1)} (A1).'
    return dict(stem=stem, answer=ans, markingKey=key, marks=5 if slot.d >= 4 and be else 4)


@R.add('ch01-st5', 'C1', (1, 3), 'mcq')
def cloud_mcq(rng, slot):
    items = [('a web-based email service used by staff', 'SaaS'), ('renting virtual machines and installing your own OS', 'IaaS'),
             ('deploying a Python web app to a managed runtime that scales automatically', 'PaaS'), ('an online accounting package used through a browser', 'SaaS'),
             ('renting block storage and virtual networks to build a custom cluster', 'IaaS'), ('a managed database-and-runtime service on which developers build apps', 'PaaS'),
             ('a video-conferencing application accessed over the internet', 'SaaS')]
    what, a = rng.choice(items)
    return nmcq(rng, f'Which cloud service model best describes {what}?', a, ['SaaS', 'PaaS', 'IaaS', 'On-premises hosting'], f'{a}: see who manages the OS and application.')


K.ar('ch01-st5', [
    ('Cloud services can scale quickly to meet demand.', 'Cloud providers have large pools of virtualised resources that can be allocated on demand.', 0, 'Both true; virtualised resource pools enable scaling.'),
    ('In SaaS the customer patches the operating system.', 'SaaS applications run on servers owned by the provider.', 3, 'A false – the provider manages the OS in SaaS; R true.'),
    ('IaaS gives the customer more control than PaaS.', 'In IaaS the customer manages the operating system and runtime.', 0, 'Both true; managing the OS is the extra control.'),
    ('Cloud computing removes all security risks.', 'Cloud providers employ specialist security staff.', 3, 'A false – risks such as misconfiguration and breaches remain; R true.'),
])


# =============================================================================================
# ch02 A1.2 Data representation and computer logic
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('binary', 'the base-2 number system, which uses only the digits 0 and 1, each representing a power of 2'),
           ('hexadecimal', 'the base-16 number system using the digits 0-9 and A-F, where each hex digit represents exactly four bits'),
           ('bit', 'a single binary digit, 0 or 1 – the smallest unit of data'),
           ('byte', 'a group of 8 bits'),
           ('nibble', 'a group of 4 bits, equal to one hexadecimal digit'),
           ('two\'s complement', 'a way of representing signed integers in which the most significant bit has a negative place value'),
           ('overflow', 'an error that occurs when the result of a calculation is too large to be stored in the available number of bits')],
    facts=[('What is the largest unsigned integer that can be stored in 8 bits?', '255', ['256', '127', '128'], '2^8 − 1 = 255.'),
           ('How many bits are represented by four hexadecimal digits?', '16', ['4', '8', '32'], 'Each hex digit is 4 bits.'),
           ('What range of integers can 8-bit two\'s complement represent?', '−128 to +127', ['−127 to +128', '0 to 255', '−255 to +255'], 'The MSB has value −128.'),
           ('Why do programmers often use hexadecimal instead of binary?', 'It is shorter and easier for humans to read, and converts directly to binary', ['Computers process hexadecimal faster', 'It uses less memory', 'It avoids overflow'], 'Hex is a human shorthand; the computer still stores binary.')],
    why=[('Explain why computers use binary to represent data.', 'Digital circuits are built from transistors that have two reliable states (on/off, high/low voltage), so two-symbol binary can be stored and processed reliably and simply.'),
         ('Explain why hexadecimal is used for colour codes and memory addresses.', 'Each hex digit maps to exactly 4 bits, so long binary values (e.g. 24-bit colours, 32/64-bit addresses) become short, readable codes with less chance of transcription error.'),
         ('Explain why adding two positive numbers in 8-bit two\'s complement can give a negative result.', 'If the true sum exceeds +127 it overflows into the sign bit, setting the MSB to 1, so the stored pattern is read as a negative number.')],
    contrast=[('unsigned binary', 'two\'s complement', 'Unsigned binary treats every bit as positive, so 8 bits give 0-255; two\'s complement gives the MSB a negative weight (−128), so 8 bits give −128 to +127 and allow negative numbers.'),
              ('a bit', 'a byte', 'A bit is a single binary digit; a byte is a group of 8 bits, the usual unit for addressing memory and measuring file size.')],
    misc=[('Hexadecimal saves memory because it uses fewer digits than binary.', 'Hex is only a human-readable notation; the computer stores the same binary bits regardless.'),
          ('In two\'s complement, 10000000 represents −0.', 'Two\'s complement has only one zero; 10000000 represents −128.'),
          ('1 KB is always exactly 1000 bytes in every context.', 'Computing often uses binary prefixes: 1 KiB = 1024 bytes; SI kilobyte = 1000 bytes; the context must be stated.')],
    evaluate=[('Hexadecimal is no longer needed now that programming languages are high level.', ['high-level code hides memory addresses and bit patterns', 'most developers rarely write binary directly'], ['hex is still used for colour codes, MAC/IPv6 addresses, memory dumps and debugging', 'error codes and machine code are shown in hex'], 'Hex remains essential wherever bit patterns are shown to humans, though less common in everyday application coding.')],
    extended=[('Show how −45 is represented in 8-bit two\'s complement, then add it to +100 in binary, explaining how the carry is handled and how to check whether overflow has occurred.', '+45 = 00101101; invert → 11010010; +1 → 11010011 = −45. 100 = 01100100. Sum: 01100100 + 11010011 = 1 00110111; discard carry out → 00110111 = 55 (correct). Overflow occurs only if two numbers with the same sign give a result with a different sign; here signs differ, so no overflow.', 6)],
))


def _tc(v, bits=8):
    return format(v & (2 ** bits - 1), f'0{bits}b')


@R.add('ch02-st1', 'C3', (1, 4), 'short')
def base_convert(rng, slot):
    hi = 255 if slot.d <= 3 else 65535
    v = rng.randint(17, hi)
    kind = rng.choice(['d2b', 'b2d', 'd2h', 'h2d', 'b2h', 'h2b'])
    b = bin(v)[2:]
    b = b.zfill(((len(b) + 3) // 4) * 4)
    h = format(v, 'X')
    q = {'d2b': (f'Convert the denary number {v} to binary.', b), 'b2d': (f'Convert the binary number {b} to denary.', str(v)),
         'd2h': (f'Convert the denary number {v} to hexadecimal.', h), 'h2d': (f'Convert the hexadecimal number {h} to denary.', str(v)),
         'b2h': (f'Convert the binary number {b} to hexadecimal.', h), 'h2b': (f'Convert the hexadecimal number {h} to binary.', b)}[kind]
    work = f'{v} = ' + ' + '.join(str(2 ** i) for i in range(len(bin(v)) - 3, -1, -1) if v >> i & 1)
    return dict(stem=q[0] + (' Show your working.' if slot.d >= 3 else ''), answer=q[1], markingKey=f'{q[1]}. Working: {work}; hex groups of 4 bits: {" ".join(b[i:i + 4] for i in range(0, len(b), 4))} → {h}.', marks=2)


@R.add('ch02-st1', 'C3', (2, 5), 'short')
def twos(rng, slot):
    bits = 8 if slot.d <= 4 else rng.choice([8, 12])
    lo, hi = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
    kind = rng.choice(['enc', 'dec', 'add'])
    if kind == 'enc':
        v = rng.randint(lo, -1)
        p = _tc(v, bits)
        return dict(stem=f'Represent {v} in {bits}-bit two\'s complement. Show your working.', answer=p,
                    markingKey=f'+{-v} = {_tc(-v, bits)} (M1); invert and add 1 (M1) → {p} (A1).', marks=3)
    if kind == 'dec':
        v = rng.randint(lo, hi)
        p = _tc(v, bits)
        return dict(stem=f'The {bits}-bit pattern {p} is a two\'s complement integer. State its denary value.', answer=str(v),
                    markingKey=f'MSB weight −{2 ** (bits - 1)}; value = {v} (A1 for value, M1 for method).', marks=2)
    a, b = rng.randint(lo // 2, hi), rng.randint(lo, hi)
    s = a + b
    stored = (s + 2 ** (bits - 1)) % 2 ** bits - 2 ** (bits - 1)
    ov = stored != s
    return dict(stem=f'Add {_tc(a, bits)} and {_tc(b, bits)}, which are {bits}-bit two\'s complement integers. Give the {bits}-bit result and state whether overflow has occurred.',
                answer=f'{_tc(s, bits)} ({"overflow – the true sum " + str(s) + " is out of range" if ov else "= " + str(s) + ", no overflow"})',
                markingKey=f'{a} + {b} = {s}; {bits}-bit result {_tc(s, bits)} read as {stored} (A1); overflow: {"yes" if ov else "no"} because {"both operands have the same sign but the result sign differs" if ov else "the result is within " + str(lo) + " to " + str(hi)} (R1).', marks=3)


@R.add('ch02-st1', 'C1', (1, 3), 'mcq')
def bits_needed(rng, slot):
    n = rng.choice([5, 12, 30, 50, 100, 200, 500, 1000, 3000])
    k = math.ceil(math.log2(n))
    ctx = rng.choice(['different product codes', 'students who each need a unique ID', 'distinct sensor states', 'seats in a stadium section'])
    return nmcq(rng, f'What is the minimum number of bits needed to give a unique binary code to each of {n} {ctx}?', str(k),
                [str(k - 1), str(k + 1), str(k + 2), str(n // 8)], f'2^{k - 1} = {2 ** (k - 1)} < {n} ≤ 2^{k} = {2 ** k}.')


@R.add('ch02-st1', 'C3', (2, 4), 'short')
def bin_shift(rng, slot):
    v = rng.randint(3, 60)
    k = rng.randint(1, 2)
    d = rng.choice(['left', 'right'])
    r = (v << k) & 255 if d == 'left' else v >> k
    return dict(stem=f'The unsigned 8-bit value {format(v, "08b")} is shifted logically {k} place{"s" if k > 1 else ""} to the {d}. State the result in binary and denary, and the arithmetic effect of the shift.',
                answer=f'{format(r, "08b")} = {r}; {"multiplied" if d == "left" else "integer-divided"} by {2 ** k}',
                markingKey=f'{format(r, "08b")} (A1) = {r} (A1); a {d} shift by {k} {"multiplies" if d == "left" else "divides (discarding the remainder)"} by 2^{k} (R1).', marks=3)


K.ar('ch02-st1', [
    ('The hexadecimal number FF equals 255 in denary.', 'Each hexadecimal digit represents four bits.', 1, 'Both true, but the 4-bit grouping does not itself explain the value (15×16 + 15).'),
    ('In 8-bit two\'s complement, 11111111 represents −1.', 'The most significant bit has a place value of −128.', 0, 'Both true: −128 + 127 = −1.'),
    ('Shifting a binary number one place to the left halves it.', 'Each place value in binary is twice the one to its right.', 3, 'A false – a left shift doubles; R true.'),
    ('8 bits can store 256 different values.', 'The largest 8-bit unsigned number is 256.', 2, 'A true; R false – the largest is 255.'),
])


R.facts('ch02-st2', F(
    terms=[('character set', 'a defined list of characters together with the binary code that represents each one, such as ASCII or Unicode'),
           ('ASCII', 'a 7-bit character set representing 128 characters: English letters, digits, punctuation and control codes'),
           ('Unicode', 'a character set that can represent over a million characters from all writing systems, encoded as UTF-8, UTF-16 or UTF-32'),
           ('colour depth', 'the number of bits used to represent the colour of each pixel'),
           ('resolution', 'the number of pixels in an image, given as width × height'),
           ('sample rate', 'the number of samples of an analogue sound wave taken per second, measured in hertz'),
           ('bit depth (audio)', 'the number of bits used to store each sound sample, which determines the precision of its amplitude'),
           ('pixel', 'the smallest addressable element of a bitmap image, which has one colour')],
    facts=[('An image uses a colour depth of 8 bits. How many different colours can it contain?', '256', ['8', '16', '255'], '2^8 = 256 colours.'),
           ('Why was Unicode introduced?', 'ASCII could not represent the characters of most of the world\'s languages', ['ASCII used too many bits per character', 'Unicode is faster to process', 'ASCII could not store digits'], 'Unicode covers scripts such as Chinese, Arabic, Devanagari and emoji.'),
           ('The ASCII code for "A" is 65. What is the ASCII code for "E"?', '69', ['68', '70', '101'], 'Letters are consecutive: A=65, B=66, … E=69.'),
           ('Which change increases the quality of recorded sound but also the file size?', 'Increasing the sample rate', ['Using lossy compression', 'Reducing the bit depth', 'Recording in mono instead of stereo'], 'More samples per second capture the waveform more accurately.')],
    why=[('Explain why increasing the colour depth of an image increases its file size.', 'Each pixel is stored using more bits, so for the same number of pixels the total number of bits (width × height × colour depth) increases.'),
         ('Explain why a higher sample rate produces a more accurate digital sound recording.', 'Samples are taken more often, so the stored values follow the shape of the analogue wave more closely and higher frequencies can be captured (Nyquist: sample rate ≥ 2 × highest frequency).'),
         ('Explain why metadata is stored in an image file.', 'The file must record width, height and colour depth (and possibly format/colour profile) so that software can interpret the stream of bits and display the pixels correctly.')],
    contrast=[('ASCII', 'Unicode', 'ASCII uses 7 bits for 128 characters (mainly English); Unicode assigns code points to over a million characters from all languages, stored in 1-4 bytes in UTF-8.'),
              ('resolution', 'colour depth', 'Resolution is the number of pixels in the image; colour depth is the number of bits used for the colour of each pixel. Both increase file size.'),
              ('sample rate', 'bit depth', 'Sample rate is how many samples are taken per second; bit depth is how many bits store each sample\'s amplitude.')],
    misc=[('Doubling the resolution of an image from 1000×1000 to 2000×2000 doubles its file size.', 'Both width and height double, so there are four times as many pixels and the file is about four times larger.'),
          ('Characters are stored in the computer as the letters themselves.', 'Each character is stored as a binary code from a character set such as ASCII or Unicode.'),
          ('A sound recorded at 44.1 kHz stores 44.1 samples per second.', '44.1 kHz means 44 100 samples per second.')],
    evaluate=[('UTF-8 is the best choice of encoding for every text file.', ['backward compatible with ASCII and uses 1 byte for English text', 'can represent every Unicode character', 'the web standard'], ['East Asian text needs 3 bytes per character, larger than UTF-16', 'variable length makes indexing the n-th character slower'], 'UTF-8 is the best default for interoperability, though UTF-16 can be more compact for some scripts.')],
    extended=[('A museum in Seoul wants to digitise 2000 photographs and 300 hours of oral-history audio. Calculate example storage requirements for chosen settings, and discuss how resolution, colour depth, sample rate and bit depth should be chosen to balance quality and storage.', 'e.g. photos 4000×3000 × 24 bits = 36 MB each → 72 GB; audio 44.1 kHz × 16 bits × 1 channel = 88.2 kB/s → 300 h ≈ 95 GB. Higher settings preserve detail for archive (lossless TIFF/FLAC), lower settings or lossy compression suffice for web access copies. Speech needs less sample rate than music (e.g. 22 kHz).', 6)],
))


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def image_size(rng, slot):
    w, h = pick(rng, [(640, 480), (800, 600), (1024, 768), (1920, 1080), (3000, 2000), (128, 128), (256, 192)])
    cd = rng.choice([1, 4, 8, 16, 24])
    bits = w * h * cd
    unit = rng.choice(['KiB', 'MiB']) if bits / 8 > 2 ** 20 else 'KiB'
    val = bits / 8 / (1024 if unit == 'KiB' else 2 ** 20)
    ctx = rng.choice(['A bitmap logo', 'A scanned page', 'A security-camera frame', 'A satellite thumbnail', 'A game sprite sheet'])
    stem = f'{ctx} is {w} × {h} pixels with a colour depth of {cd} bits. Calculate the file size in {unit}, ignoring metadata'
    ans = f'{r2(val, 2)} {unit}'
    key = f'{w} × {h} × {cd} = {bits:,} bits (M1); ÷ 8 = {bits // 8:,} bytes (M1); ÷ {1024 if unit == "KiB" else "1024²"} = {r2(val, 2)} {unit} (A1).'
    if slot.d >= 4:
        stem += f', and state how many colours can be represented'
        ans += f'; {2 ** cd:,} colours'
        key += f' Colours = 2^{cd} = {2 ** cd:,} (A1).'
    return dict(stem=stem + '.', answer=ans, markingKey=key, marks=4 if slot.d >= 4 else 3)


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def sound_size(rng, slot):
    sr = rng.choice([8000, 16000, 22050, 44100, 48000])
    bd = rng.choice([8, 16, 24])
    ch = rng.choice([1, 2])
    sec = rng.choice([10, 30, 60, 90, 180, 240])
    bits = sr * bd * ch * sec
    mb = bits / 8 / 1e6
    ctx = rng.choice(['A voice memo', 'A podcast clip', 'A music track', 'A bird-song field recording', 'An interview recording'])
    return dict(stem=f'{ctx} lasts {sec} s and is recorded at {sr} Hz with a bit depth of {bd} bits in {"mono" if ch == 1 else "stereo"}. Calculate the file size in MB (1 MB = 10^6 bytes).',
                answer=f'{r2(mb, 3)} MB', markingKey=f'{sr} × {bd} × {ch} × {sec} = {bits:,} bits (M1); ÷ 8 ÷ 10^6 = {r2(mb, 3)} MB (A1).', marks=3)


@R.add('ch02-st2', 'C3', (1, 4), 'short')
def ascii_q(rng, slot):
    word = rng.choice(['CODE', 'BYTE', 'LOOP', 'DATA', 'HASH', 'NODE', 'PIXEL', 'QUEUE', 'STACK'])
    kind = rng.choice(['codes', 'decode', 'case'])
    if kind == 'codes':
        codes = ' '.join(str(ord(c)) for c in word)
        return dict(stem=f'The ASCII code for "A" is 65 and letters are numbered consecutively. State the ASCII codes (in denary) for the characters of "{word}".', answer=codes,
                    markingKey=f'{codes} (1 mark for each two correct codes).', marks=2)
    if kind == 'decode':
        codes = ' '.join(format(ord(c), '07b') for c in word)
        return dict(stem=f'The following 7-bit ASCII codes ("A" = 1000001) spell a word: {codes}. Decode the word.', answer=word,
                    markingKey=f'{word} ({" ".join(str(ord(c)) for c in word)}).', marks=2)
    w2 = word.lower()
    return dict(stem=f'In ASCII, "A" is 65 and "a" is 97. State the ASCII codes for "{w2}" and explain how a program could convert it to upper case using the codes.',
                answer=f'{" ".join(str(ord(c)) for c in w2)}; subtract 32 from each code (or clear bit 5) to get {" ".join(str(ord(c)) for c in word)}',
                markingKey='1 mark for the codes; 1 mark for subtracting 32 / clearing bit 5.', marks=2)


@R.add('ch02-st2', 'C3', (2, 4), 'short')
def utf8_bytes(rng, slot):
    words = ['café', 'naïve', 'Zürich', 'São Paulo', 'Ελλάδα', 'Москва', 'नमस्ते', '東京', 'Ołówek', 'piñata', 'Hello']
    w = rng.choice(words)
    n = len(w.encode('utf-8'))
    return dict(stem=f'The string "{w}" has {len(w)} characters. Each character is stored in UTF-8 (ASCII characters 1 byte, most accented Latin, Greek and Cyrillic 2 bytes, most other scripts such as Devanagari and Chinese 3 bytes). Calculate the number of bytes needed and compare with UTF-32.',
                answer=f'{n} bytes in UTF-8; {4 * len(w)} bytes in UTF-32', markingKey=f'UTF-8: ' + ' + '.join(str(len(c.encode("utf-8"))) for c in w) + f' = {n} (A1); UTF-32: 4 × {len(w)} = {4 * len(w)} (A1).', marks=2)


K.ar('ch02-st2', [
    ('A 1-bit colour depth image can show only two colours.', '2^1 = 2.', 0, 'Both true; R explains A.'),
    ('UTF-8 can represent Chinese characters.', 'UTF-8 always uses exactly one byte per character.', 2, 'A true; R false – UTF-8 uses 1-4 bytes.'),
    ('Stereo sound files are about twice the size of mono files with the same settings.', 'Stereo stores a separate sample for each of two channels.', 0, 'Both true; two channels double the data.'),
    ('Reducing the sample rate increases the quality of a sound recording.', 'Sample rate is measured in hertz.', 3, 'A false; R true.'),
])


R.facts('ch02-st3', F(
    terms=[('logic gate', 'an electronic component that performs a Boolean operation on one or more binary inputs to produce a single binary output'),
           ('truth table', 'a table listing every combination of inputs to a logic circuit and the corresponding output'),
           ('AND gate', 'a gate whose output is 1 only when all of its inputs are 1'),
           ('OR gate', 'a gate whose output is 1 when at least one input is 1'),
           ('XOR gate', 'a gate whose output is 1 when exactly one of its two inputs is 1 (the inputs differ)'),
           ('NAND gate', 'a gate whose output is 0 only when all inputs are 1 – the inverse of AND; any circuit can be built from NAND gates alone'),
           ('NOT gate', 'a gate with one input whose output is the inverse of the input')],
    facts=[('How many rows does the truth table of a circuit with 3 inputs have?', '8', ['3', '6', '9'], '2^3 = 8 input combinations.'),
           ('Which gate outputs 1 only when both inputs are 0?', 'NOR', ['NAND', 'XOR', 'AND'], 'NOR is NOT OR: output 1 only when no input is 1.'),
           ('Which gate is known as a universal gate?', 'NAND', ['XOR', 'OR', 'NOT'], 'NAND (and NOR) can be combined to build every other gate.'),
           ('Which two-input gate gives the output 0 for inputs (0,0) and (1,1) and 1 otherwise?', 'XOR', ['XNOR', 'NAND', 'OR'], 'XOR is 1 when the inputs differ.')],
    why=[('Explain why NAND gates are called universal gates.', 'NOT, AND and OR can all be built from NAND gates alone (NOT A = A NAND A, etc.), and every Boolean function can be built from NOT, AND and OR, so any circuit can be made from NANDs only – simplifying manufacture.'),
         ('Explain why a truth table for n inputs has 2^n rows.', 'Each input can independently be 0 or 1, so the number of combinations doubles with each additional input: 2 × 2 × … = 2^n.'),
         ('Explain why an XOR gate is used in a half adder.', 'The sum bit of two binary digits is 1 only when exactly one input is 1 (0+1, 1+0) and 0 for 1+1 (with a carry), which is exactly the XOR function; the carry is given by AND.')],
    contrast=[('an AND gate', 'a NAND gate', 'AND outputs 1 only when all inputs are 1; NAND is its inverse, outputting 0 only when all inputs are 1.'),
              ('an OR gate', 'an XOR gate', 'OR outputs 1 when one or both inputs are 1; XOR outputs 1 only when exactly one input is 1, so it gives 0 for (1,1).')],
    misc=[('An OR gate outputs 1 only if exactly one of its inputs is 1.', 'That describes XOR; OR outputs 1 when at least one input is 1, including when both are 1.'),
          ('A NOT gate has two inputs.', 'A NOT gate has a single input and inverts it.'),
          ('NAND and NOR give the same truth table because both start with N.', 'NAND is 0 only for all-1 inputs; NOR is 1 only for all-0 inputs – the tables are different.')],
    evaluate=[('Building circuits only from NAND gates is always the best design choice.', ['a single gate type simplifies manufacture and reduces cost', 'NAND is fast in CMOS technology'], ['may need more gates than a mixed design, increasing delay', 'harder for humans to read and debug'], 'Excellent for mass production of chips, but not always optimal in gate count or clarity.')],
    extended=[('A half adder adds two bits A and B to give a sum S and a carry C. Construct its truth table, derive Boolean expressions for S and C, and explain how two half adders and an OR gate form a full adder.', 'Truth table: 00→S0C0, 01→S1C0, 10→S1C0, 11→S0C1. S = A XOR B, C = A AND B. Full adder: first half adder adds A and B; second adds the result to Cin giving the final sum; the carry out is the OR of the two half-adder carries.', 6)],
))

_GATES = {'AND': lambda a, b: a & b, 'OR': lambda a, b: a | b, 'XOR': lambda a, b: a ^ b,
          'NAND': lambda a, b: 1 - (a & b), 'NOR': lambda a, b: 1 - (a | b), 'XNOR': lambda a, b: 1 - (a ^ b)}


def _rand_expr(rng, vars_, depth):
    if depth == 0:
        v = rng.choice(vars_)
        return (('NOT', v) if rng.random() < 0.25 else v)
    g = rng.choice(['AND', 'OR', 'XOR', 'NAND', 'NOR']) if depth > 1 else rng.choice(['AND', 'OR', 'XOR', 'NAND', 'NOR', 'AND', 'OR'])
    for _ in range(10):
        l, r = _rand_expr(rng, vars_, depth - 1), _rand_expr(rng, vars_, rng.randint(0, depth - 1))
        if l != r and l != ('NOT', r) and r != ('NOT', l):
            break
    e = (g, l, r)
    return ('NOT', e) if rng.random() < 0.15 else e


def _ev(e, env):
    if isinstance(e, str):
        return env[e]
    if e[0] == 'NOT':
        return 1 - _ev(e[1], env)
    return _GATES[e[0]](_ev(e[1], env), _ev(e[2], env))


def _show(e, top=True):
    if isinstance(e, str):
        return e
    if e[0] == 'NOT':
        inner = _show(e[1], False)
        return f'NOT {inner}' if top or isinstance(e[1], str) else f'(NOT {inner})'
    s = f'{_show(e[1], False)} {e[0]} {_show(e[2], False)}'
    return s if top else f'({s})'


def _vars_in(e):
    if isinstance(e, str):
        return {e}
    return set().union(*(_vars_in(x) for x in e[1:]))


def _tt(e, vs):
    rows = []
    for bits in itertools.product([0, 1], repeat=len(vs)):
        env = dict(zip(vs, bits))
        rows.append((bits, _ev(e, env)))
    return rows


@R.add('ch02-st3', 'C3', (1, 5), 'short')
def truth_table(rng, slot):
    vs = ['A', 'B'] if slot.d <= 2 else ['A', 'B', 'C']
    for _ in range(20):
        e = _rand_expr(rng, vs, 1 if slot.d <= 2 else 2)
        if _vars_in(e) == set(vs):
            break
    else:
        return None
    rows = _tt(e, vs)
    outs = ''.join(str(o) for _, o in rows)
    if len(set(outs)) == 1:
        return None
    ask = rng.choice(['full', 'count'])
    t = table(vs + ['X'], [list(b) + [o] for b, o in rows])
    if ask == 'full':
        return dict(stem=f'Complete the truth table for X = {_show(e)} (list the output X for inputs in binary counting order, starting with all 0s).',
                    answer=f'X column: {" ".join(outs)}', markingKey=f'{t}\n1 mark for each two correct rows (max {len(rows) // 2}).', marks=len(rows) // 2)
    n1 = outs.count('1')
    return dict(stem=f'For the expression X = {_show(e)}, state the number of input combinations for which X = 1, and list them.',
                answer=f'{n1}: ' + ', '.join(''.join(map(str, b)) for b, o in rows if o), markingKey=f'Truth table:\n{t}\n1 mark for the count, 1-2 marks for the list.', marks=3)


@R.add('ch02-st3', 'C3', (1, 3), 'mcq')
def gate_from_table(rng, slot):
    g = rng.choice(list(_GATES))
    outs = ' '.join(str(_GATES[g](a, b)) for a, b in itertools.product([0, 1], repeat=2))
    return nmcq(rng, f'A two-input gate gives these outputs for inputs AB = 00, 01, 10, 11: {outs}. Which gate is it?', g,
                rng.sample([x for x in _GATES if x != g], 3), f'{g} gives {outs}.')


@R.add('ch02-st3', 'C3', (2, 4), 'short')
def gate_inputs(rng, slot):
    vs = ['A', 'B', 'C']
    for _ in range(20):
        e = _rand_expr(rng, vs, 2)
        if _vars_in(e) == set(vs):
            break
    env = {v: rng.randint(0, 1) for v in vs}
    out = _ev(e, env)
    inner = []
    def walk(x):
        if isinstance(x, str):
            return
        for y in x[1:]:
            walk(y)
        inner.append(f'{_show(x)} = {_ev(x, env)}')
    walk(e)
    return dict(stem=f'A circuit computes X = {_show(e)}. Determine the output X when A = {env["A"]}, B = {env["B"]} and C = {env["C"]}, showing the value at each gate.',
                answer=str(out), markingKey='Intermediate values: ' + '; '.join(inner) + f'. Final X = {out}. 1 mark for intermediate values, 1 mark for the output.', marks=2)


K.ar('ch02-st3', [
    ('A NAND gate outputs 0 only when all of its inputs are 1.', 'NAND is the inverse of AND.', 0, 'Both true; inverting AND gives this behaviour.'),
    ('A 4-input circuit has 16 rows in its truth table.', 'Each input doubles the number of input combinations.', 0, 'Both true; 2^4 = 16.'),
    ('XOR outputs 1 when both inputs are 1.', 'XOR is used to compute the sum bit in a half adder.', 3, 'A false (XOR gives 0 for 1,1); R true.'),
    ('NOT gates can be built from a single NAND gate.', 'NAND has a single input.', 2, 'A true (tie inputs together); R false – NAND has two or more inputs.'),
])


R.facts('ch02-st4', F(
    terms=[('Boolean expression', 'an expression built from Boolean variables and the operators AND, OR and NOT (and derived operators) that evaluates to true or false'),
           ('logic circuit', 'a network of connected logic gates that implements a Boolean expression'),
           ('De Morgan\'s laws', 'the rules NOT (A AND B) = NOT A OR NOT B and NOT (A OR B) = NOT A AND NOT B'),
           ('combinational circuit', 'a logic circuit whose output depends only on its current inputs, with no memory of previous inputs'),
           ('half adder', 'a circuit that adds two bits, giving a sum (A XOR B) and a carry (A AND B)')],
    facts=[('Which expression is equivalent to NOT (A AND B)?', 'NOT A OR NOT B', ['NOT A AND NOT B', 'A OR B', 'NOT A AND B'], 'De Morgan\'s law.'),
           ('A light turns on when switch S is on and either sensor P or sensor Q detects movement. Which expression describes it?', 'S AND (P OR Q)', ['(S AND P) OR Q', 'S OR P OR Q', 'S AND P AND Q'], 'The brackets ensure S is needed in both cases.'),
           ('In Boolean algebra, what is A AND NOT A?', '0', ['1', 'A', 'NOT A'], 'A variable and its inverse can never both be 1.'),
           ('What is the output of a combinational circuit determined by?', 'Only the current inputs', ['The previous outputs', 'The clock speed', 'The order the inputs changed'], 'Combinational circuits have no memory.')],
    why=[('Explain why brackets are important when writing a Boolean expression from a problem description.', 'AND is usually evaluated before OR, so without brackets "A AND B OR C" means (A AND B) OR C; brackets ensure the expression matches the intended conditions, otherwise the circuit gives wrong outputs for some inputs.'),
         ('Explain how a truth table can be used to check that a circuit matches a specification.', 'Every input combination is listed and the output of the circuit is calculated for each and compared with the required output; if all rows match the circuit is correct, because a combinational circuit\'s behaviour is completely described by its truth table.'),
         ('Explain why De Morgan\'s laws are useful when building circuits.', 'They let an expression be rewritten using different gates, e.g. turning OR into NAND with inverted inputs, so circuits can be built from one gate type (NAND/NOR) or simplified.')],
    contrast=[('a Boolean expression', 'a logic circuit', 'A Boolean expression is the algebraic description of a function; a logic circuit is the physical arrangement of gates that implements it. Each can be derived from the other.'),
              ('NOT (A OR B)', 'NOT A OR NOT B', 'NOT (A OR B) is 1 only when both are 0 (equal to NOT A AND NOT B); NOT A OR NOT B is 1 unless both are 1 (equal to NOT (A AND B)).')],
    misc=[('NOT (A AND B) is the same as NOT A AND NOT B.', 'By De Morgan\'s law NOT (A AND B) = NOT A OR NOT B; the AND changes to OR.'),
          ('A OR A equals 2A.', 'Boolean values are only 0 or 1; A OR A = A (idempotent law).'),
          ('Two circuits with different gates must have different truth tables.', 'Different circuits can be logically equivalent (e.g. a NAND-only version of an OR circuit) and have identical truth tables.')],
    evaluate=[('Truth tables are the best way to verify a logic circuit.', ['exhaustive – every input combination is checked', 'simple and mechanical'], ['grows as 2^n rows, impractical for many inputs', 'gives no insight into how to simplify the circuit'], 'Ideal for small circuits; algebra, K-maps or automated tools are needed for larger ones.')],
    extended=[('A greenhouse vent V must open if the temperature is high (T) and it is not raining (R), or if humidity is high (H) regardless of the rain. Write a Boolean expression for V, construct its truth table and describe a logic circuit that implements it.', 'V = (T AND NOT R) OR H. Truth table (T,R,H → V): 000→0, 001→1, 010→0, 011→1, 100→1, 101→1, 110→0, 111→1. Circuit: NOT gate on R, AND gate with T and NOT R, OR gate combining that output with H.', 6)],
))

_SCEN = [
    ('An alarm A sounds when the system is armed (S) and either a door (D) or a window (W) is opened.', 'S AND (D OR W)', ('AND', 'S', ('OR', 'D', 'W'))),
    ('A car warning light L comes on if the engine is running (E) and either a seat belt is not fastened (B = 0) or a door is open (D).', 'E AND (NOT B OR D)', ('AND', 'E', ('OR', ('NOT', 'B'), 'D'))),
    ('A vending machine releases a drink R when a coin is inserted (C) and a selection is made (S), but not if the machine is empty (E).', 'C AND S AND NOT E', ('AND', ('AND', 'C', 'S'), ('NOT', 'E'))),
    ('A sprinkler P turns on when the soil is dry (D) and it is night (N), or when manual override (M) is pressed.', '(D AND N) OR M', ('OR', ('AND', 'D', 'N'), 'M')),
    ('A lift motor M may run only if the doors are closed (C) and the lift is not overloaded (O).', 'C AND NOT O', ('AND', 'C', ('NOT', 'O'))),
    ('A heater H turns on when the room is cold (C) and someone is present (P), unless a window is open (W).', 'C AND P AND NOT W', ('AND', ('AND', 'C', 'P'), ('NOT', 'W'))),
    ('A safety light F flashes when exactly one of two sensors X and Y is triggered (a sensor fault).', 'X XOR Y', ('XOR', 'X', 'Y')),
    ('A press P operates only when both hand buttons L and R are pressed and the guard G is closed.', 'L AND R AND G', ('AND', ('AND', 'L', 'R'), 'G')),
    ('A pump Q switches on if the tank is low (L) or the pressure is low (P), but never when the maintenance switch (M) is on.', '(L OR P) AND NOT M', ('AND', ('OR', 'L', 'P'), ('NOT', 'M'))),
]


@R.add('ch02-st4', 'C3', (1, 5), 'short')
def scenario_expr(rng, slot):
    txt, expr, tree = rng.choice(_SCEN)
    vs = sorted(_vars_in(tree))
    rows = _tt(tree, vs)
    if slot.d <= 2:
        return dict(stem=f'{txt} Write a Boolean expression for the output.', answer=expr, markingKey=f'{expr} (1 mark per correctly combined condition; brackets must be correct).', marks=2)
    t = table(vs + ['Out'], [list(b) + [o] for b, o in rows])
    n1 = sum(o for _, o in rows)
    return dict(stem=f'{txt} Write a Boolean expression for the output and state how many of the {len(rows)} input combinations make the output 1.',
                answer=f'{expr}; {n1} combinations', markingKey=f'{expr} (2 marks). Truth table:\n{t}\n{n1} rows give 1 (1 mark).', marks=3)


def _describe(e):
    gates, cnt = [], [0]
    def walk(x):
        if isinstance(x, str):
            return x
        if x[0] == 'NOT':
            a = walk(x[1])
            cnt[0] += 1
            gates.append(f'G{cnt[0]} is a NOT gate with input {a}')
            return f'G{cnt[0]}'
        a, b = walk(x[1]), walk(x[2])
        cnt[0] += 1
        gates.append(f'G{cnt[0]} is a {x[0]} gate with inputs {a} and {b}')
        return f'G{cnt[0]}'
    walk(e)
    return gates


@R.add('ch02-st4', 'C3', (2, 5), 'short')
def circuit_expr(rng, slot):
    vs = ['A', 'B', 'C']
    for _ in range(30):
        e = _rand_expr(rng, vs, 2 if slot.d <= 3 else 3)
        if _vars_in(e) == set(vs) and 3 <= len(_describe(e)) <= 5:
            break
    else:
        return None
    g = _describe(e)
    env = {v: rng.randint(0, 1) for v in vs}
    return dict(stem=f'A logic circuit is described gate by gate: {"; ".join(g)}. The output X is taken from G{len(g)}. Write a Boolean expression for X and find X when A = {env["A"]}, B = {env["B"]}, C = {env["C"]}.',
                answer=f'X = {_show(e)}; X = {_ev(e, env)}', markingKey=f'X = {_show(e)} (2 marks, 1 for partial); value {_ev(e, env)} (1 mark).', marks=3)


_EQUIV = [(('NOT', ('AND', 'A', 'B')), ('OR', ('NOT', 'A'), ('NOT', 'B'))), (('NOT', ('OR', 'A', 'B')), ('AND', ('NOT', 'A'), ('NOT', 'B'))),
          (('NOT', ('AND', 'A', 'B')), ('AND', ('NOT', 'A'), ('NOT', 'B'))), (('OR', 'A', ('AND', 'A', 'B')), 'A'),
          (('AND', 'A', ('OR', 'A', 'B')), 'A'), (('OR', ('AND', 'A', 'B'), ('AND', 'A', ('NOT', 'B'))), 'A'),
          (('XOR', 'A', 'B'), ('OR', ('AND', 'A', ('NOT', 'B')), ('AND', ('NOT', 'A'), 'B'))), (('XOR', 'A', 'B'), ('OR', 'A', 'B')),
          (('OR', ('NOT', 'A'), 'B'), ('NOT', ('AND', 'A', ('NOT', 'B')))), (('AND', ('OR', 'A', 'B'), ('OR', 'A', 'C')), ('OR', 'A', ('AND', 'B', 'C'))),
          (('NAND', 'A', 'A'), ('NOT', 'A')), (('NOR', 'A', 'B'), ('NOT', ('AND', 'A', 'B')))]


@R.add('ch02-st4', 'C2', (2, 4), 'explain')
def equiv(rng, slot):
    a, b = rng.choice(_EQUIV)
    vs = sorted(_vars_in(a) | _vars_in(b))
    ra, rb = _tt(a, vs), _tt(b, vs)
    same = all(x[1] == y[1] for x, y in zip(ra, rb))
    diff = [''.join(map(str, x[0])) for x, y in zip(ra, rb) if x[1] != y[1]]
    return dict(stem=f'Use a truth table to determine whether X = {_show(a)} and Y = {_show(b)} are logically equivalent. Explain your conclusion.',
                answer='Equivalent – identical outputs for every input combination' if same else f'Not equivalent – they differ for input(s) {", ".join(diff)}',
                markingKey=table(vs + ['X', 'Y'], [list(x[0]) + [x[1], y[1]] for x, y in zip(ra, rb)]) + ('\nAll rows match (equivalent).' if same else f'\nRows {", ".join(diff)} differ.') + ' 2 marks for the table, 1 for the conclusion.', marks=3)


K.ar('ch02-st4', [
    ('NOT (A OR B) is equivalent to NOT A AND NOT B.', 'De Morgan\'s laws swap AND and OR when a NOT is distributed over brackets.', 0, 'Both true; R is the law applied.'),
    ('A AND (A OR B) simplifies to A.', 'This is an example of the absorption law.', 0, 'Both true; absorption is the reason.'),
    ('A combinational circuit can remember its previous output.', 'The output of a combinational circuit depends only on its current inputs.', 3, 'A false; R true and contradicts A.'),
    ('A AND NOT A always equals 0.', 'A variable cannot be 1 and 0 at the same time.', 0, 'Both true; R explains A.'),
    ('A OR B is equivalent to A XOR B.', 'XOR outputs 0 when both inputs are 1.', 3, 'A false (they differ for 1,1); R true.'),
])


# ---- ch02-st5 Boolean algebra and Karnaugh maps (HL) ----
import sympy as _sp
from sympy.logic.boolalg import simplify_logic as _simp, SOPform as _sop

_SYM = {v: _sp.Symbol(v) for v in 'ABCD'}


def _to_ib(expr):
    s = str(expr)
    s = s.replace('~', 'NOT ').replace(' & ', ' AND ').replace(' | ', ' OR ')
    return s


def _mint_sop(vs, minterms):
    return _sop([_SYM[v] for v in vs], [list(map(int, format(m, f'0{len(vs)}b'))) for m in minterms])


R.facts('ch02-st5', F(
    terms=[('Karnaugh map (K-map)', 'a grid representation of a truth table, ordered in Gray code, in which adjacent 1s are grouped in powers of two to simplify a Boolean expression'),
           ('minterm', 'a product (AND) term containing every input variable exactly once, either plain or inverted, that is 1 for exactly one input combination'),
           ('sum of products (SOP)', 'a Boolean expression written as an OR of AND terms'),
           ('Gray code', 'an ordering of binary values in which consecutive values differ in only one bit, used for K-map row and column labels'),
           ('absorption law', 'the identities A + A·B = A and A·(A + B) = A'),
           ('don\'t care condition', 'an input combination that cannot occur or whose output does not matter, so it can be treated as 0 or 1 when grouping in a K-map')],
    facts=[('In a K-map, groups of 1s must contain…', 'a power of two cells (1, 2, 4, 8…)', ['any number of cells', 'exactly three cells', 'only cells in the same row'], 'Only groups of 2^k cells eliminate k variables.'),
           ('Why are K-map rows labelled 00, 01, 11, 10 rather than 00, 01, 10, 11?', 'So adjacent cells differ by only one variable (Gray code)', ['To save space', 'Because 11 is larger than 10', 'To list minterms in denary order'], 'Adjacency must mean a one-bit change so that grouping eliminates a variable.'),
           ('Simplify A·B + A·NOT B.', 'A', ['B', 'A·B', '1'], 'A(B + NOT B) = A·1 = A.'),
           ('A group of four 1s in a 4-variable K-map eliminates how many variables?', '2', ['1', '3', '4'], '4 = 2^2, so two variables change within the group.')],
    why=[('Explain why grouping adjacent 1s in a K-map simplifies an expression.', 'Adjacent cells differ in exactly one variable, so within a group that variable appears both as 1 and 0 and cancels (X·Y + X·NOT Y = X); larger groups cancel more variables, giving fewer gates.'),
         ('Explain why simplifying Boolean expressions matters when building circuits.', 'A simpler expression needs fewer gates and connections, so the circuit is cheaper, smaller, uses less power and has less propagation delay.'),
         ('Explain why groups in a K-map may wrap around the edges.', 'The map is effectively a torus: the first and last rows/columns differ in only one bit in Gray code, so they are adjacent and can be grouped.')],
    contrast=[('Boolean algebra simplification', 'K-map simplification', 'Boolean algebra applies laws step by step and works for any number of variables but needs insight; K-maps are a visual method that reliably finds a minimal SOP for up to about four variables.'),
              ('a minterm', 'a sum-of-products expression', 'A minterm is one AND term covering exactly one input row with all variables present; an SOP is an OR of AND terms, which may be minterms or simplified products.')],
    misc=[('In a K-map you may group three adjacent 1s.', 'Groups must contain a power of two cells; three 1s need two overlapping groups of two.'),
          ('A K-map group should be as small as possible to keep the expression accurate.', 'Groups should be as large as possible (while containing only 1s), since larger groups eliminate more variables and give a simpler, still correct, expression.'),
          ('A + A·B simplifies to A·B.', 'By absorption A + A·B = A(1 + B) = A.')],
    evaluate=[('K-maps are the most effective method for simplifying logic expressions.', ['visual, quick and reliable for up to four variables', 'easy to spot don\'t-care conditions'], ['impractical beyond five or six variables', 'software tools (Quine-McCluskey, Espresso) scale better'], 'Best for small hand-designed circuits; algorithmic tools are better for real chip design.')],
    extended=[('A 3-input function F(A, B, C) is 1 for the input combinations 001, 011, 101 and 111. Draw a K-map, simplify F, and prove the result with Boolean algebra.', 'All four 1s lie where C = 1, forming one group of four: F = C. Algebra: F = A\'B\'C + A\'BC + AB\'C + ABC = A\'C(B\' + B) + AC(B\' + B) = A\'C + AC = C(A\' + A) = C.', 6)],
))


@R.add('ch02-st5', 'C3', (2, 5), 'short')
def kmap_simplify(rng, slot):
    n = 3 if slot.d <= 3 else rng.choice([3, 4])
    vs = list('ABCD'[:n])
    for _ in range(30):
        ms = sorted(rng.sample(range(2 ** n), rng.randint(3, 2 ** n - 3 if n == 3 else 8)))
        sop = _mint_sop(vs, ms)
        if len(str(sop)) < 5 * len(ms) and sop not in (_sp.true, _sp.false):
            break
    s = _to_ib(sop)
    rows = '\n'.join(f'{format(m, f"0{n}b")}' for m in ms)
    return dict(stem=f'A function F({", ".join(vs)}) equals 1 only for these input combinations ({"".join(vs)}): {", ".join(format(m, f"0{n}b") for m in ms)}. Use a Karnaugh map to find a minimal sum-of-products expression for F.',
                answer=f'F = {s}', markingKey=f'Correct K-map with 1s in cells {", ".join(map(str, ms))} (1 mark); correct groups (1-2 marks); F = {s} (1 mark). Any equivalent minimal SOP is accepted.', marks=4)


_ALG = ['(A & B) | (A & ~B)', '(A | B) & (A | ~B)', 'A | (A & B)', '~(~A & ~B)', '(A & B) | (~A & B) | (A & ~B)',
        '(A & B & C) | (A & B & ~C)', '~(A | B) | (~A & B)', '(A | B) & ~(A & B) & A', '(A & ~B) | (A & B & C) | (A & ~C)',
        '~(A & ~B) & B', '(A | B | C) & (A | B | ~C)', '(~A & ~B & C) | (~A & B & C) | (A & ~B & C)', '(A & ~(B | C)) | (A & B)']


@R.add('ch02-st5', 'C3', (2, 5), 'short')
def algebra_simplify(rng, slot):
    src = rng.choice(_ALG)
    e = _sp.sympify(src, locals=_SYM)
    s = _simp(e, form='dnf')
    return dict(stem=f'Simplify the Boolean expression {_to_ib(src.replace("(", "( ").replace(")", " )")).replace("( ", "(").replace(" )", ")")} using the laws of Boolean algebra, naming the laws you use.',
                answer=_to_ib(s), markingKey=f'Final result {_to_ib(s)} (A1); M1 for each correct, named law (e.g. distributive, complement A + NOT A = 1, identity A·1 = A, absorption, De Morgan). Equivalent forms accepted.', marks=4)


@R.add('ch02-st5', 'C3', (1, 4), 'short')
def minterms_of(rng, slot):
    vs = ['A', 'B', 'C']
    for _ in range(20):
        e = _rand_expr(rng, vs, 2)
        if _vars_in(e) == set(vs):
            break
    rows = _tt(e, vs)
    ms = [int(''.join(map(str, b)), 2) for b, o in rows if o]
    if not 1 <= len(ms) <= 6:
        return None
    terms = [' AND '.join(v if bit else f'NOT {v}' for v, bit in zip(vs, b)) for b, o in rows if o]
    return dict(stem=f'Write X = {_show(e)} as a sum of minterms (canonical sum of products), giving the minterm numbers.',
                answer=f'm({", ".join(map(str, ms))}): ' + ' OR '.join(f'({t})' for t in terms), markingKey=f'Truth table rows with X = 1: {", ".join(map(str, ms))} (1-2 marks); correct minterms (1 mark).', marks=3)


K.ar('ch02-st5', [
    ('A·B + A·NOT B simplifies to A.', 'B + NOT B = 1.', 0, 'Both true; the complement law gives A·1 = A.'),
    ('A K-map group of eight cells in a 4-variable map leaves a single variable.', 'Each doubling of a group size eliminates one variable.', 0, 'Both true: 8 = 2^3, so 3 of 4 variables are eliminated.'),
    ('K-map rows are labelled in normal binary order.', 'Adjacent cells must differ in only one variable.', 3, 'A false (Gray code is used); R true – which is why.'),
    ('Groups in a K-map may overlap.', 'A K-map has one cell for each row of the truth table.', 1, 'Both true, but the cell layout is not why overlap is allowed; overlapping lets each group be as large as possible.'),
])


# =============================================================================================
# ch03 A1.3 Operating systems and control systems
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('operating system (OS)', 'system software that manages the hardware and software resources of a computer and provides services and an interface to programs and users'),
           ('memory management', 'the OS function that allocates and frees main memory for processes, keeps processes separate and manages virtual memory'),
           ('process management', 'the OS function that creates, schedules and terminates processes and shares CPU time between them'),
           ('file management', 'the OS function that organises files in directories, controls access permissions and maps files to storage blocks'),
           ('device driver', 'software that lets the OS communicate with a particular hardware device through a standard interface'),
           ('paging', 'dividing memory into equal-sized frames and processes into pages of the same size so that a process need not occupy contiguous memory'),
           ('kernel', 'the core of the operating system that runs in privileged mode and controls memory, processes and hardware access')],
    facts=[('Which OS function prevents one program from overwriting another program\'s memory?', 'Memory management (memory protection)', ['File management', 'User interface', 'Device driver installation'], 'The OS gives each process its own address space.'),
           ('A new printer works after installing software supplied by the manufacturer. What is this software?', 'A device driver', ['A compiler', 'A utility program', 'Firmware for the CPU'], 'Drivers translate generic OS requests into device-specific commands.'),
           ('Which OS function decides which process uses the CPU next?', 'Process scheduling', ['Paging', 'File allocation', 'Authentication'], 'The scheduler is part of process management.'),
           ('Which of these is NOT normally a function of the operating system?', 'Editing spreadsheet formulas', ['Managing virtual memory', 'Handling interrupts', 'Controlling user access rights'], 'Spreadsheet editing is done by application software.')],
    why=[('Explain why an operating system is needed between application programs and the hardware.', 'It hides hardware details behind standard services (system calls, drivers), shares the CPU, memory and devices between programs safely, and protects programs from each other, so applications do not need to manage hardware themselves.'),
         ('Explain why paging allows more programs to run than would fit in RAM.', 'Only the pages a process is currently using need to be in RAM; other pages stay in virtual memory on disk and are swapped in when needed, and pages need not be contiguous.'),
         ('Explain why user accounts and permissions are part of the OS.', 'The OS controls all access to files and devices, so it is the only place where it can reliably authenticate users and enforce who may read, write or execute each resource.')],
    contrast=[('paging', 'segmentation', 'Paging splits memory into fixed-size pages/frames invisible to the programmer; segmentation splits a program into variable-sized logical segments (code, data, stack).'),
              ('the kernel', 'the user interface', 'The kernel is the privileged core that manages resources; the user interface (GUI or CLI) is the part users interact with to give commands.')],
    misc=[('The OS is only needed when the computer starts up.', 'The OS runs continuously, managing processes, memory, files, devices and interrupts the whole time the computer is on.'),
          ('Each program must contain its own code to drive the printer.', 'Programs send requests to the OS, which uses the printer\'s device driver; applications do not drive hardware directly.'),
          ('Paging requires each process to be stored in one continuous block of RAM.', 'Paging allows pages to be placed in any free frames, so a process can be scattered across memory.')],
    evaluate=[('An embedded system such as a washing machine does not need an operating system.', ['a single fixed task can run as one program loop', 'removing the OS reduces cost, memory and boot time'], ['complex devices (smart TVs, cars) need multitasking, networking and drivers', 'a real-time OS makes timing guarantees easier'], 'Simple embedded devices often run without an OS, but more complex or connected embedded systems benefit from a (real-time) OS.')],
    extended=[('A smartphone runs a music app, a navigation app and a messaging app at once. Describe how the operating system\'s process management, memory management and device management functions allow this.', 'Process management: each app is a process; the scheduler shares CPU time (time slices, priorities, background vs foreground). Memory: each process gets its own protected address space; paging/virtual memory and suspending background apps free RAM. Devices: drivers give shared access to speaker, GPS and network; the OS arbitrates (e.g. audio focus) and handles interrupts from each device.', 6)],
))

_OS_TASKS = [('allocating RAM to a newly opened program', 'memory management'), ('swapping an inactive page to disk', 'memory management'),
             ('deciding which ready process runs next', 'process management (scheduling)'), ('terminating a program that has stopped responding', 'process management'),
             ('creating a folder and setting read-only permission on it', 'file management'), ('tracking which disk blocks belong to a file', 'file management'),
             ('sending data to a printer through its driver', 'device (peripheral) management'), ('handling a keyboard interrupt', 'device management / interrupt handling'),
             ('checking a user\'s password at log-in', 'security (user management)'), ('displaying windows and icons', 'user interface')]


@R.add('ch03-st1', 'C3', (1, 3), 'short')
def os_classify(rng, slot):
    ts = rng.sample(_OS_TASKS, 3)
    ans = '; '.join(f'{t} – {f}' for t, f in ts)
    return dict(stem=f'Identify the operating system function responsible for each task: {"; ".join(t for t, _ in ts)}.', answer=ans,
                markingKey=f'1 mark each: {ans}.', marks=3)


@R.add('ch03-st1', 'C3', (2, 5), 'numerical')
def paging(rng, slot):
    ps = rng.choice([256, 512, 1024, 2048, 4096])
    npages = rng.randint(4, 7)
    frames = rng.sample(range(2, 30), npages)
    page = rng.randrange(npages)
    off = rng.randrange(ps)
    la = page * ps + off
    pa = frames[page] * ps + off
    pt = ', '.join(f'page {i} → frame {f}' for i, f in enumerate(frames))
    return dict(stem=f'A system uses paging with a page size of {ps} bytes. A process\'s page table is: {pt}. Translate the logical address {la} into a physical address.',
                answer=str(pa), markingKey=f'Page = {la} DIV {ps} = {page} (M1); offset = {la} MOD {ps} = {off} (M1); frame {frames[page]} → physical = {frames[page]} × {ps} + {off} = {pa} (A1).', marks=3)


K.ar('ch03-st1', [
    ('The OS allocates memory to processes.', 'Memory management keeps each process\'s memory separate and protected.', 0, 'Both true; R is the function that does A.'),
    ('A device driver is part of the application software.', 'A driver lets the OS communicate with a specific hardware device.', 3, 'A false – drivers are system software used by the OS; R true.'),
    ('Paging lets a process be stored in non-contiguous frames.', 'Pages and frames have the same fixed size.', 0, 'Both true; equal sizes let any page fit in any free frame.'),
])


R.facts('ch03-st2', F(
    terms=[('scheduling', 'the OS activity of deciding which process in the ready queue gets the CPU and for how long'),
           ('first come, first served (FCFS)', 'a non-preemptive scheduling algorithm that runs processes to completion in order of arrival'),
           ('round robin (RR)', 'a preemptive scheduling algorithm in which each ready process gets a fixed time slice (quantum) in turn'),
           ('priority scheduling', 'an algorithm in which the ready process with the highest priority runs next'),
           ('starvation', 'a situation in which a low-priority process waits indefinitely because other processes are always chosen first'),
           ('multilevel queue scheduling', 'scheduling in which processes are placed in separate queues (e.g. system, interactive, batch), each with its own algorithm and priority'),
           ('waiting time', 'the total time a process spends in the ready queue, equal to turnaround time minus burst time'),
           ('preemption', 'the OS interrupting a running process to give the CPU to another process')],
    facts=[('Which scheduling algorithm can suffer from the convoy effect, where short jobs wait behind one long job?', 'FCFS', ['Round robin', 'Shortest job first', 'Multilevel feedback queue'], 'FCFS never preempts the long job.'),
           ('Which technique prevents starvation in priority scheduling?', 'Ageing – gradually raising the priority of waiting processes', ['Increasing the time quantum', 'Using FCFS for all processes', 'Reducing the number of processes'], 'Ageing guarantees every process eventually runs.'),
           ('What happens in round robin if the time quantum is very large?', 'It behaves like FCFS', ['It becomes shortest job first', 'Context switches increase', 'Processes starve'], 'Each process finishes within one quantum, in arrival order.'),
           ('Which scheduling algorithm gives the minimum average waiting time when all jobs arrive together?', 'Shortest job first', ['FCFS', 'Round robin', 'Priority by user ID'], 'Running short jobs first reduces total waiting.')],
    why=[('Explain why round robin is suitable for interactive, time-sharing systems.', 'Each process gets the CPU regularly for a short quantum, so no user waits long for a response, giving fair and responsive service even with long jobs present.'),
         ('Explain why a very small round-robin time quantum reduces efficiency.', 'Every switch requires a context switch (saving/restoring registers and state), which is overhead; with tiny quanta a large share of CPU time is spent switching rather than running processes.'),
         ('Explain why multilevel queue scheduling is used in modern operating systems.', 'Different processes have different needs: system and interactive tasks need fast response (high priority, RR), batch jobs need throughput (lower priority, FCFS); separate queues let the OS apply the right policy to each class.')],
    contrast=[('preemptive scheduling', 'non-preemptive scheduling', 'In preemptive scheduling the OS can interrupt a running process (e.g. quantum expires, higher priority arrives); in non-preemptive scheduling a process keeps the CPU until it finishes or blocks.'),
              ('FCFS', 'round robin', 'FCFS runs each process to completion in arrival order (simple, convoy effect); round robin gives each process a fixed time slice in turn (fair, responsive, more context switches).')],
    misc=[('Round robin always gives the lowest average waiting time.', 'RR is fair and responsive but often has higher average waiting/turnaround than SJF because of interleaving and context switches.'),
          ('In priority scheduling, a low-priority process is guaranteed to run eventually.', 'Without ageing, a steady stream of higher-priority processes can cause starvation.'),
          ('FCFS is preemptive because it handles processes in order.', 'FCFS is non-preemptive: once a process starts it runs until it finishes or blocks.')],
    evaluate=[('Round robin is the best scheduling algorithm for all operating systems.', ['fair, no starvation, good response time for interactive users'], ['context-switch overhead', 'ignores priorities – unsuitable for real-time tasks', 'higher average turnaround than SJF for batch work'], 'Good for time-sharing, but real systems combine it with priorities (multilevel feedback queues).')],
    extended=[('A hospital server runs real-time patient-monitoring alerts, interactive staff queries and overnight report generation. Recommend a scheduling strategy, justifying how it handles each type of process and how starvation is avoided.', 'Multilevel (feedback) queue: highest-priority queue for real-time alerts (preemptive priority), middle queue for interactive queries (round robin with short quantum for responsiveness), lowest for batch reports (FCFS/long quantum). Ageing promotes long-waiting batch jobs so they are not starved; reports scheduled overnight when load is low.', 6)],
))


def _schedule(procs, algo, q=2):
    """procs: list of (name, arrival, burst, priority). Returns (gantt list of (name, start, end), completion dict)."""
    t, done, gantt = 0, {}, []
    rem = {p[0]: p[2] for p in procs}
    arr = {p[0]: p[1] for p in procs}
    pri = {p[0]: p[3] for p in procs}
    order = [p[0] for p in sorted(procs, key=lambda p: (p[1], p[0]))]
    if algo == 'RR':
        ready, i = deque(), 0
        while len(done) < len(procs):
            while i < len(order) and arr[order[i]] <= t:
                ready.append(order[i]); i += 1
            if not ready:
                t = arr[order[i]]
                continue
            n = ready.popleft()
            run = min(q, rem[n])
            gantt.append((n, t, t + run))
            t += run
            rem[n] -= run
            while i < len(order) and arr[order[i]] <= t:
                ready.append(order[i]); i += 1
            if rem[n] == 0:
                done[n] = t
            else:
                ready.append(n)
        return gantt, done
    while len(done) < len(procs):
        avail = [n for n in order if n not in done and arr[n] <= t]
        if not avail:
            t = min(arr[n] for n in order if n not in done)
            continue
        if algo == 'FCFS':
            n = avail[0]
        elif algo == 'SJF':
            n = min(avail, key=lambda x: (rem[x], arr[x]))
        else:
            n = min(avail, key=lambda x: (pri[x], arr[x]))
        gantt.append((n, t, t + rem[n]))
        t += rem[n]
        done[n] = t
    return gantt, done


_ALGO_TXT = {'FCFS': 'first come, first served (FCFS)', 'SJF': 'non-preemptive shortest job first (SJF)',
             'PRI': 'non-preemptive priority scheduling (1 = highest priority)', 'RR': 'round robin'}


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def sched(rng, slot):
    n = 3 if slot.d <= 2 else 4 if slot.d <= 4 else 5
    names = ['P1', 'P2', 'P3', 'P4', 'P5'][:n]
    arrivals = sorted([0] + [rng.randint(0, 8) for _ in range(n - 1)])
    procs = [(names[i], arrivals[i], rng.randint(1, 9), rng.randint(1, 5)) for i in range(n)]
    algo = rng.choice(['FCFS', 'SJF', 'PRI', 'RR', 'RR'])
    q = rng.choice([2, 3, 4])
    gantt, done = _schedule(procs, algo, q)
    wait = {p[0]: done[p[0]] - p[1] - p[2] for p in procs}
    avg = sum(wait.values()) / n
    show_pri = algo == 'PRI'
    tab = table(['Process', 'Arrival', 'Burst'] + (['Priority'] if show_pri else []), [[p[0], p[1], p[2]] + ([p[3]] if show_pri else []) for p in procs])
    g = ' | '.join(f'{a} {s}-{e}' for a, s, e in gantt)
    alg = _ALGO_TXT[algo] + (f' with a time quantum of {q}' if algo == 'RR' else '')
    rr_rule = ' (a process arriving at the same moment a quantum ends joins the queue before the preempted process)' if algo == 'RR' else ''
    return dict(stem=f'The processes below are scheduled using {alg}{rr_rule}.\n{tab}\nDraw the Gantt chart (as time intervals) and calculate the waiting time of each process and the average waiting time.',
                answer=f'Gantt: {g}. Waiting: ' + ', '.join(f'{k} {v}' for k, v in wait.items()) + f'; average {r2(avg)}',
                markingKey=f'Gantt chart {g} (2 marks). Waiting time = completion − arrival − burst: ' + ', '.join(f'{p[0]}: {done[p[0]]} − {p[1]} − {p[2]} = {wait[p[0]]}' for p in procs) + f' (2 marks); average = {sum(wait.values())}/{n} = {r2(avg)} (1 mark).', marks=5)


@R.add('ch03-st2', 'C3', (2, 4), 'short')
def sched_compare(rng, slot):
    bursts = [rng.randint(1, 12) for _ in range(3)]
    procs = [(f'J{i + 1}', 0, b, 1) for i, b in enumerate(bursts)]
    res = {}
    for a in ('FCFS', 'SJF'):
        _, done = _schedule(procs, a)
        res[a] = sum(done[p[0]] - p[2] for p in procs) / 3
    if res['FCFS'] == res['SJF']:
        return None
    return dict(stem=f'Three jobs arrive at time 0 in the order J1, J2, J3 with burst times {bursts[0]}, {bursts[1]} and {bursts[2]} ms. Calculate the average waiting time under FCFS and under shortest job first, and explain the difference.',
                answer=f'FCFS {r2(res["FCFS"])} ms, SJF {r2(res["SJF"])} ms; SJF is lower because short jobs no longer wait behind long ones',
                markingKey=f'FCFS average {r2(res["FCFS"])} (A1), SJF average {r2(res["SJF"])} (A1), explanation that running shorter jobs first reduces the total waiting of the others (R1).', marks=3)


K.ar('ch03-st2', [
    ('Round robin prevents starvation.', 'Every ready process receives a time slice in turn.', 0, 'Both true; cyclic service is the reason.'),
    ('Non-preemptive priority scheduling can cause starvation.', 'High-priority processes are always selected before lower-priority ones.', 0, 'Both true; R explains A.'),
    ('FCFS gives good response times for interactive users.', 'FCFS runs each process to completion before starting the next.', 3, 'A false – long jobs delay others; R true and is why A is false.'),
    ('A smaller time quantum always improves CPU efficiency.', 'Each context switch takes CPU time.', 3, 'A false – more switches add overhead; R true.'),
])


R.facts('ch03-st3', F(
    terms=[('polling', 'a method in which the CPU repeatedly checks the status of a device at regular intervals to see whether it needs attention'),
           ('interrupt', 'a signal from hardware or software to the CPU that an event needs immediate attention, causing the current task to be suspended'),
           ('interrupt service routine (ISR)', 'the code executed by the CPU to handle a particular interrupt'),
           ('interrupt priority', 'a ranking that decides which interrupt is handled first and whether one ISR may be interrupted by another'),
           ('context switch', 'saving the state (registers, PC) of the current process so another task can run, and later restoring it')],
    facts=[('When an interrupt is accepted, what does the CPU do first?', 'Saves the contents of the PC and registers (e.g. on the stack)', ['Restarts the computer', 'Deletes the current process', 'Increases the clock speed'], 'The state must be saved so the interrupted task can resume.'),
           ('When does the CPU check for interrupts?', 'At the end of each fetch-decode-execute cycle', ['Only at start-up', 'Every second', 'Only when the program finishes'], 'Interrupts are checked between instructions.'),
           ('Which device is most suitably handled by polling?', 'A temperature sensor read every second by a simple microcontroller', ['A keyboard on a desktop PC', 'A network card receiving packets', 'A power-failure detector'], 'Regular, predictable sampling suits polling.'),
           ('Which interrupt should have the highest priority?', 'Power failure', ['Printer out of paper', 'Key pressed', 'Timer for screen saver'], 'It needs immediate action to save data before power is lost.')],
    why=[('Explain why interrupts are more efficient than polling for a keyboard.', 'Key presses are infrequent and unpredictable; with polling the CPU wastes cycles checking when nothing has happened, while with interrupts the CPU does other work and only responds when a key is actually pressed.'),
         ('Explain why the contents of the registers are saved before an interrupt service routine runs.', 'The ISR will use the registers; saving the PC and registers lets the CPU restore them afterwards so the interrupted program continues exactly where it left off, unaware it was interrupted.'),
         ('Explain why polling can be preferable in a simple, time-critical embedded system.', 'Polling is simple and deterministic: the device is checked at known times, avoiding the unpredictable latency and overhead of interrupt handling, which matters for fixed-rate control loops.')],
    contrast=[('polling', 'interrupts', 'With polling the CPU repeatedly checks devices whether or not they need attention (wasting cycles); with interrupts the device signals the CPU only when it needs attention, so the CPU can do other work.'),
              ('a hardware interrupt', 'a software interrupt', 'A hardware interrupt is generated by a device (keyboard, timer, I/O completion); a software interrupt is generated by a program, e.g. a system call or an exception such as division by zero.')],
    misc=[('An interrupt immediately stops the instruction currently being executed halfway through.', 'The CPU finishes the current fetch-decode-execute cycle and checks for interrupts at the end of it.'),
          ('Polling is always worse than interrupts.', 'Polling is simple and predictable and is efficient when events are frequent and regular; interrupts are better for rare, unpredictable events.'),
          ('After an ISR finishes, the interrupted program must restart from the beginning.', 'The saved PC and registers are restored so the program resumes exactly where it stopped.')],
    evaluate=[('Interrupts should be used for every input device.', ['CPU does useful work instead of checking idle devices', 'fast response to rare events'], ['each interrupt has overhead for saving/restoring state', 'very frequent events (high-speed data) can overwhelm the CPU (interrupt storm) – DMA or polling may be better', 'polling gives deterministic timing'], 'Interrupts suit most infrequent inputs, but high-rate or timing-critical devices may be better served by polling or DMA.')],
    extended=[('A smart thermostat must read a temperature sensor, respond to the user pressing buttons and receive commands from a phone app over Wi-Fi. For each input, recommend polling or interrupts and justify; then describe what happens when the button interrupt arrives while the CPU is processing a Wi-Fi command.', 'Sensor: polling at a fixed interval (regular, predictable). Buttons: interrupt (rare, needs quick response). Wi-Fi: interrupt when a packet arrives. When the button interrupt arrives: CPU completes the current instruction, checks priority; if higher than the current ISR it saves PC/registers, runs the button ISR, restores state and resumes the Wi-Fi handling; otherwise it is queued until the current ISR finishes.', 6)],
))


@R.add('ch03-st3', 'C3', (2, 5), 'numerical')
def poll_overhead(rng, slot):
    f = rng.choice([50, 100, 200, 500]) * 10 ** 6
    cycles = rng.choice([50, 100, 200, 400])
    rate = rng.choice([60, 100, 500, 1000, 10000, 50000])
    dev = rng.choice(['mouse', 'keyboard', 'temperature sensor', 'network interface', 'barcode scanner'])
    pct = cycles * rate / f * 100
    return dict(stem=f'A {f // 10 ** 6} MHz processor polls a {dev} {rate} times per second; each poll takes {cycles} clock cycles. Calculate the percentage of CPU time spent polling' + (' and comment on whether polling is appropriate.' if slot.d >= 4 else '.'),
                answer=f'{r2(pct, 4)}%', markingKey=f'Cycles per second = {cycles} × {rate} = {cycles * rate:,} (M1); ÷ {f:,} × 100 = {r2(pct, 4)}% (A1).' + (f' Comment: {"negligible overhead, polling acceptable" if pct < 1 else "significant overhead – interrupts (or DMA) would be better"} (R1).' if slot.d >= 4 else ''), marks=3 if slot.d >= 4 else 2)


@R.add('ch03-st3', 'C3', (3, 5), 'short')
def isr_order(rng, slot):
    devs = rng.sample([('power failure', 1), ('disk read complete', 2), ('network packet', 3), ('timer', 4), ('keyboard', 5), ('printer ready', 6)], 3)
    events = []
    t = 0
    for d_, p in devs:
        events.append((t, d_, p, rng.randint(2, 6)))
        t += rng.randint(1, 4)
    # preemptive priority simulation of ISRs (lower number = higher priority)
    clock, active, finished, pend = 0, [], [], list(events)
    rem = {e[1]: e[3] for e in events}
    while len(finished) < len(events):
        for e in [e for e in pend if e[0] <= clock]:
            active.append(e); pend.remove(e)
        if not active:
            clock = pend[0][0]; continue
        cur = min(active, key=lambda e: e[2])
        rem[cur[1]] -= 1
        clock += 1
        if rem[cur[1]] == 0:
            active.remove(cur); finished.append((cur[1], clock))
    lst = '; '.join(f'at t = {e[0]} ms a "{e[1]}" interrupt (priority {e[2]}, ISR takes {e[3]} ms)' for e in events)
    return dict(stem=f'Interrupts are prioritised (1 = highest) and a higher-priority interrupt pre-empts a running ISR of lower priority. The CPU is idle when these occur: {lst}. State the order in which the ISRs finish and the time each finishes.',
                answer=', '.join(f'{n} at {c} ms' for n, c in finished), markingKey='Order and finishing times: ' + ', '.join(f'{n} at {c} ms' for n, c in finished) + '. 1 mark for the correct order, 1-2 marks for the times; pre-empted ISRs resume after higher-priority ones complete.', marks=3)


K.ar('ch03-st3', [
    ('Interrupts allow the CPU to do other work while waiting for a slow device.', 'The device signals the CPU only when it needs attention.', 0, 'Both true; R explains A.'),
    ('The CPU checks for interrupts at the end of each FDE cycle.', 'Instructions must complete so that the processor state is consistent when it is saved.', 0, 'Both true; R gives the reason.'),
    ('Polling uses no CPU time when no device needs attention.', 'In polling the CPU repeatedly checks each device\'s status.', 3, 'A false – checking idle devices wastes CPU time; R true.'),
])


R.facts('ch03-st4', F(
    terms=[('multitasking', 'the ability of an OS to run several processes apparently at the same time by rapidly switching the CPU between them'),
           ('deadlock', 'a situation in which two or more processes are each waiting for a resource held by another, so none can proceed'),
           ('mutual exclusion', 'the condition that a resource can be used by only one process at a time'),
           ('hold and wait', 'the condition in which a process holds at least one resource while waiting to acquire another'),
           ('circular wait', 'a closed chain of processes in which each waits for a resource held by the next'),
           ('resource allocation graph', 'a directed graph showing which processes hold which resources and which resources processes are waiting for'),
           ('race condition', 'an error in which the result depends on the unpredictable order in which concurrent processes access shared data')],
    facts=[('Which set of conditions must ALL hold for deadlock to occur (Coffman conditions)?', 'Mutual exclusion, hold and wait, no preemption and circular wait', ['Starvation, paging and interrupts', 'Mutual exclusion and round robin only', 'High priority and long burst time'], 'Removing any one condition prevents deadlock.'),
           ('Requiring processes to request all their resources at once prevents deadlock by removing which condition?', 'Hold and wait', ['Mutual exclusion', 'Circular wait', 'No preemption'], 'A process never holds some resources while waiting for others.'),
           ('Numbering resources and requiring requests in increasing order prevents…', 'circular wait', ['mutual exclusion', 'starvation in round robin', 'paging faults'], 'A cycle would need a request for a lower-numbered resource.'),
           ('On a single-core CPU, multitasking is achieved by…', 'rapid context switching between processes', ['running all processes simultaneously', 'using a separate RAM for each process', 'turning off interrupts'], 'Only one process runs at an instant; switching gives the illusion of concurrency.')],
    why=[('Explain why deadlock cannot occur if circular wait is prevented.', 'Deadlock requires a cycle of processes each waiting for the next; if resources must be requested in a fixed global order, no process can wait for a resource earlier in the order than one it holds, so a cycle can never form.'),
         ('Explain why a race condition can corrupt a shared bank balance.', 'Two processes may both read the old balance before either writes; each then writes its own update, so one update is lost – the result depends on timing. Locks (mutual exclusion) make read-modify-write atomic.'),
         ('Explain why operating systems often ignore deadlock (the "ostrich" approach).', 'Prevention and avoidance add overhead and restrict resource use, while deadlocks are rare in many desktop systems; it can be cheaper to restart the affected processes when it happens.')],
    contrast=[('deadlock', 'starvation', 'In deadlock a set of processes all wait on each other in a cycle and none can ever proceed; in starvation a process waits indefinitely because others keep being chosen, though the system as a whole progresses.'),
              ('deadlock prevention', 'deadlock avoidance', 'Prevention removes one of the necessary conditions by design (e.g. ordered requests); avoidance checks each request at run time (e.g. Banker\'s algorithm) and grants it only if the system stays in a safe state.')],
    misc=[('Deadlock happens whenever a process has to wait for a resource.', 'Waiting is normal; deadlock needs a circular chain of processes each holding a resource the next one needs.'),
          ('Multitasking means a single-core CPU executes several instructions from different programs at the same instant.', 'A single core executes one instruction stream at a time; multitasking is achieved by rapid switching.'),
          ('Restarting the computer is the only way to recover from deadlock.', 'The OS can abort one process in the cycle or preempt a resource and roll a process back.')],
    evaluate=[('Deadlock avoidance using the Banker\'s algorithm is practical for a general-purpose OS.', ['guarantees deadlock never occurs', 'allows more concurrency than strict prevention'], ['processes must declare maximum resource needs in advance – rarely known', 'checking every request is costly with many processes and resources'], 'Rarely practical for desktop OSs; more suited to systems with known, fixed resource needs.')],
    extended=[('Two print jobs each need the printer (R1) and a scanner (R2). Job A holds R1 and requests R2; job B holds R2 and requests R1. Explain why this is a deadlock with reference to the four necessary conditions, and describe two different ways the OS could prevent or recover from it.', 'Mutual exclusion (devices non-shareable), hold and wait (each holds one, wants another), no preemption (cannot take a device away mid-job), circular wait (A→R2→B→R1→A). Prevention: request both devices at once, or order resources so all jobs request R1 before R2. Recovery: abort one job or preempt its device and roll it back.', 6)],
))


def _cycle(edges):
    """edges: dict node -> list of nodes; return a cycle list or None."""
    color, stack = {}, []
    def dfs(u):
        color[u] = 1; stack.append(u)
        for v in edges.get(u, []):
            if color.get(v) == 1:
                return stack[stack.index(v):] + [v]
            if v not in color:
                r = dfs(v)
                if r:
                    return r
        color[u] = 2; stack.pop()
        return None
    for n in sorted(edges):
        if n not in color:
            r = dfs(n)
            if r:
                return r
    return None


@R.add('ch03-st4', 'C3', (2, 5), 'short')
def deadlock_detect(rng, slot):
    n = 3 if slot.d <= 3 else 4
    ps = [f'P{i + 1}' for i in range(n)]
    rs = [f'R{i + 1}' for i in range(n)]
    holds = {p: r for p, r in zip(ps, rng.sample(rs, n))}
    owner = {r: p for p, r in holds.items()}
    wants = {}
    for p in ps:
        if rng.random() < 0.85:
            wants[p] = rng.choice([r for r in rs if r != holds[p]])
    wf = {p: [owner[wants[p]]] for p in wants}
    cyc = _cycle(wf)
    desc = '; '.join(f'{p} holds {holds[p]}' + (f' and requests {wants[p]}' if p in wants else '') for p in ps)
    ans = f'Deadlock: {" → ".join(cyc)}' if cyc else 'No deadlock: the wait-for graph has no cycle'
    return dict(stem=f'Each resource has a single instance. {desc}. Draw the wait-for graph and determine whether the system is deadlocked; if so, identify the processes involved.',
                answer=ans, markingKey='Wait-for edges: ' + ', '.join(f'{p} → {wf[p][0]}' for p in wf) + f'. {ans}. 1 mark for the graph, 1 for the conclusion, 1 for identifying the cycle (or explaining why none).', marks=3)


@R.add('ch03-st4', 'C3', (3, 5), 'short')
def bankers(rng, slot):
    for _ in range(50):
        n, m = 4, 3
        mx = [[rng.randint(1, 7) for _ in range(m)] for _ in range(n)]
        al = [[rng.randint(0, mx[i][j]) for j in range(m)] for i in range(n)]
        av = [rng.randint(0, 4) for _ in range(m)]
        need = [[mx[i][j] - al[i][j] for j in range(m)] for i in range(n)]
        work, fin, seq = av[:], [False] * n, []
        progress = True
        while progress:
            progress = False
            for i in range(n):
                if not fin[i] and all(need[i][j] <= work[j] for j in range(m)):
                    work = [work[j] + al[i][j] for j in range(m)]
                    fin[i] = True; seq.append(f'P{i}'); progress = True
        if (all(fin) and rng.random() < 0.7) or (not all(fin) and seq):
            break
    tab = table(['Process', 'Allocated (A B C)', 'Maximum (A B C)'], [[f'P{i}', ' '.join(map(str, al[i])), ' '.join(map(str, mx[i]))] for i in range(n)])
    safe = all(fin)
    ans = f'Safe; safe sequence {", ".join(seq)}' if safe else f'Unsafe: after {", ".join(seq)} no remaining process can have its need met'
    return dict(stem=f'Using the Banker\'s algorithm, the available resources are A = {av[0]}, B = {av[1]}, C = {av[2]}.\n{tab}\nCalculate the Need matrix and determine whether the system is in a safe state (check processes in order P0, P1, P2, P3 repeatedly).',
                answer=ans, markingKey='Need = Max − Allocated: ' + '; '.join(f'P{i} {" ".join(map(str, need[i]))}' for i in range(n)) + f' (2 marks). {ans} (2 marks).', marks=4)


K.ar('ch03-st4', [
    ('Deadlock requires a circular wait.', 'In a circular wait each process holds a resource needed by the next process in the chain.', 0, 'Both true; R explains why the cycle is needed.'),
    ('Ordering resource requests prevents deadlock.', 'Ordering makes a circular wait impossible.', 0, 'Both true; R explains A.'),
    ('Starvation and deadlock are the same thing.', 'In both, a process may wait for a long time.', 3, 'A false; R true.'),
    ('Locks can prevent race conditions.', 'Locks allow only one process at a time into a critical section.', 0, 'Both true; mutual exclusion is the reason.'),
])


R.facts('ch03-st5', F(
    terms=[('control system', 'a system that manages the behaviour of a device or process by processing inputs from sensors and sending signals to actuators'),
           ('sensor', 'an input device that measures a physical quantity such as temperature, light or pressure and converts it to an electrical signal'),
           ('actuator', 'an output device, such as a motor, valve, pump or heater, that produces a physical action in response to a control signal'),
           ('feedback', 'using the measured output of a system as an input, so that the controller can adjust its actions to reach the set point'),
           ('embedded system', 'a computer system with a dedicated function built into a larger device, often with real-time constraints'),
           ('set point', 'the target value that a control system tries to maintain, such as 21 °C'),
           ('closed-loop control', 'control in which the output is measured and fed back to the controller to correct errors'),
           ('analogue-to-digital converter (ADC)', 'a component that converts a continuous analogue sensor signal into digital values the processor can use')],
    facts=[('In an automatic greenhouse watering system, which component is the actuator?', 'The water pump/valve', ['The soil-moisture sensor', 'The microcontroller', 'The set point'], 'The actuator acts on the environment.'),
           ('Why is an ADC needed in many control systems?', 'Sensors produce analogue signals but the processor works with digital data', ['Actuators need analogue input from memory', 'To increase clock speed', 'To store the program'], 'Analogue voltages must be sampled and digitised.'),
           ('A traffic light that changes on a fixed timer, regardless of traffic, is an example of…', 'open-loop control', ['closed-loop control', 'negative feedback', 'a sensor network'], 'No measurement of traffic is fed back.'),
           ('Which is an example of negative feedback?', 'A thermostat switches the heater off when the temperature rises above the set point', ['A microphone near a speaker producing a howl', 'A fixed-time washing cycle', 'A counter that only increases'], 'Negative feedback acts to reduce the error.')],
    why=[('Explain why feedback is essential in a cruise-control system.', 'Road gradient and wind change the car\'s speed; the speed sensor feeds the actual speed back so the controller compares it with the set speed and adjusts the throttle, keeping speed constant despite disturbances.'),
         ('Explain why embedded systems often have real-time requirements.', 'They control physical processes (airbags, braking, insulin pumps) where a response after a deadline is useless or dangerous, so they must guarantee responses within fixed time limits.'),
         ('Explain why a thermostat uses a small band (hysteresis) around the set point.', 'If the heater switched exactly at the set point it would turn on and off very rapidly due to noise and small fluctuations, wearing out the relay; a band (e.g. on below 20 °C, off above 22 °C) prevents this.')],
    contrast=[('open-loop control', 'closed-loop control', 'Open-loop control acts without measuring the result (e.g. timed sprinkler); closed-loop control measures the output with sensors and feeds it back to correct deviations from the set point.'),
              ('a sensor', 'an actuator', 'A sensor is an input device that measures a physical quantity; an actuator is an output device that causes a physical change.')],
    misc=[('A sensor decides when to switch the heater on.', 'The sensor only measures; the microprocessor compares the reading with the set point and decides, then signals the actuator.'),
          ('Embedded systems are always simple and never connected to networks.', 'Many embedded systems (smart meters, cars, IoT devices) are complex and networked.'),
          ('Closed-loop systems keep the output exactly at the set point at all times.', 'They correct deviations after they are measured, so the output fluctuates around the set point.')],
    evaluate=[('Computer-controlled systems are safer than human-controlled ones.', ['respond faster and consistently, never tired', 'continuous monitoring with precise sensors'], ['sensor failure or software bugs can cause dangerous behaviour', 'cannot handle unexpected situations outside their design', 'vulnerable to cyberattack if networked'], 'Often safer for routine, well-defined tasks, but human oversight and fail-safes remain essential.')],
    extended=[('Design an automatic control system for an ICU incubator that keeps a baby\'s environment at 36.5 °C and 60% humidity. Identify the sensors, actuators and processing, describe the feedback loop, and explain two safety features.', 'Sensors: temperature, humidity (and possibly skin temperature); ADCs convert readings. Processor compares readings with set points every second. Actuators: heater, humidifier, fan; alarm. Loop: read → compare → adjust heater/humidifier → repeat (negative feedback, hysteresis). Safety: redundant sensors and range checks; alarm and fail-safe shutdown if readings are out of range or a sensor fails; manual override.', 6)],
))


@R.add('ch03-st5', 'C3', (2, 5), 'short')
def thermostat(rng, slot):
    lo = rng.choice([18, 19, 20, 21])
    hi = lo + rng.choice([1, 2])
    t = rng.choice([lo - 2, lo - 1, lo, hi])
    heat = t < lo
    rise, fall = rng.choice([0.5, 1.0, 1.5]), rng.choice([0.5, 1.0])
    steps = 5 + slot.d
    rows = []
    for k in range(steps):
        if t < lo:
            heat = True
        elif t > hi:
            heat = False
        rows.append((k, t, 'ON' if heat else 'OFF'))
        t = round(t + (rise if heat else -fall), 1)
    tab = ' | '.join(f'{k}: {r2(tt, 1)} °C {h}' for k, tt, h in rows)
    ons = sum(1 for r in rows if r[2] == 'ON')
    return dict(stem=f'A heater controller reads the temperature each minute: if T < {lo} °C it switches the heater ON; if T > {hi} °C it switches it OFF; otherwise it leaves it unchanged. The heater starts {"ON" if rows[0][2] == "ON" and rows[0][1] >= lo else "OFF"} and T starts at {rows[0][1]} °C. While ON the temperature rises {rise} °C per minute; while OFF it falls {fall} °C per minute. Trace minutes 0 to {steps - 1}, giving T and the heater state after each decision, and state for how many of these minutes the heater is ON.',
                answer=f'{tab}; ON for {ons} minutes', markingKey=f'Trace: {tab}. 1 mark per two correct rows (max 3); count {ons} (1 mark).', marks=4)


_CTRL = [('an automatic greenhouse window', 'temperature sensor, rain sensor', 'motor that opens/closes the window'),
         ('a car\'s anti-lock braking system', 'wheel-speed sensors', 'hydraulic valves that release brake pressure'),
         ('a street light', 'light (LDR) sensor', 'relay that switches the lamp'),
         ('an automatic door', 'infrared/motion sensor', 'electric motor that slides the door'),
         ('a home burglar alarm', 'PIR motion sensor, magnetic door contacts', 'siren and flashing light'),
         ('a smart irrigation system', 'soil-moisture sensor', 'solenoid valve/pump'),
         ('a washing machine', 'water-level (pressure) sensor, temperature sensor', 'heater, drum motor and inlet valve'),
         ('an aquarium controller', 'pH and temperature sensors', 'heater and dosing pump')]


@R.add('ch03-st5', 'C3', (1, 4), 'short')
def ctrl_parts(rng, slot):
    sys_, sens, act = rng.choice(_CTRL)
    return dict(stem=f'For {sys_}, identify suitable sensor(s) and actuator(s), and describe how feedback is used to control it.',
                answer=f'Sensors: {sens}. Actuators: {act}. Feedback: the processor repeatedly reads the sensors (via an ADC), compares the values with set points and signals the actuators to correct any difference; the new readings show the effect.',
                markingKey=f'Sensor(s): {sens} (1); actuator(s): {act} (1); feedback loop – read, compare with set point, act, repeat (1-2).', marks=4)


K.ar('ch03-st5', [
    ('A thermostat is an example of closed-loop control.', 'It measures the temperature and uses it to decide whether to switch the heater.', 0, 'Both true; feeding the measurement back is what makes it closed-loop.'),
    ('An actuator converts a physical quantity into an electrical signal.', 'Actuators are output devices.', 3, 'A false – that describes a sensor; R true.'),
    ('An ADC is needed between an analogue sensor and a microprocessor.', 'Microprocessors process digital values.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch04 A1.4 Translation (HL)
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('compiler', 'a translator that converts the whole of a high-level source program into machine code (an executable) before it is run'),
           ('interpreter', 'a translator that analyses and executes a high-level program one statement at a time, without producing a separate executable'),
           ('source code', 'the program as written by the programmer in a high-level language'),
           ('object code', 'the machine-code output of a compiler, which may need linking before it can run'),
           ('assembler', 'a translator that converts assembly-language mnemonics into machine code, usually one instruction for each mnemonic'),
           ('machine code', 'binary instructions that a particular processor can execute directly')],
    facts=[('Which translator stops at the first error it meets during execution?', 'An interpreter', ['A compiler', 'An assembler', 'A linker'], 'An interpreter executes line by line, so it halts when it reaches an error.'),
           ('Why is compiled software usually distributed without its source code?', 'The executable runs without the compiler and the source (intellectual property) is kept secret', ['Compilers delete the source code', 'Source code cannot be copied', 'Executables are always smaller than source code'], 'Users only need the machine code.'),
           ('Which is an advantage of an interpreter during development?', 'Code can be tested immediately, line by line, without a separate compile step', ['The program runs faster', 'The source code is hidden', 'No translator is needed at run time'], 'Quick edit-run cycles help debugging.'),
           ('A compiled executable built for an x86 Windows PC will…', 'not run directly on an ARM-based phone', ['run on any processor', 'run faster on an interpreter', 'automatically recompile itself'], 'Machine code is specific to an instruction set and OS.')],
    why=[('Explain why a compiled program usually runs faster than the same program interpreted.', 'Translation is done once in advance and the compiler can optimise the whole program, so at run time the CPU executes machine code directly, whereas an interpreter must analyse each statement every time it is executed (e.g. inside loops).'),
         ('Explain why interpreted programs are more portable than compiled executables.', 'The same source code can run on any machine that has an interpreter for that language; a compiled executable contains machine code for one processor and OS.'),
         ('Explain why a compiler can report all the syntax errors in a program at once.', 'It analyses the entire source code before any of it is executed, so it can continue checking after the first error and list every error with its line number.')],
    contrast=[('a compiler', 'an interpreter', 'A compiler translates the whole program into an executable before running it (fast execution, errors reported together, source hidden); an interpreter translates and runs one statement at a time (no executable, stops at the first error, slower, portable source).'),
              ('an assembler', 'a compiler', 'An assembler translates low-level assembly mnemonics into machine code largely one-to-one; a compiler translates high-level statements, each of which may become many machine instructions.')],
    misc=[('An interpreter produces an executable file that can be given to customers.', 'Interpreters do not produce an executable; the interpreter must be present every time the program is run.'),
          ('Compiled programs never contain errors because the compiler checks them.', 'Compilers detect syntax (and some semantic) errors but not logic errors or many run-time errors.'),
          ('Interpreted languages cannot be compiled.', 'Being interpreted is a property of an implementation, not the language; Python, for example, can be compiled to bytecode or to machine code with tools.')],
    evaluate=[('Developers should always use a compiled language for commercial software.', ['faster execution and source code protection', 'no interpreter needed by customers'], ['must compile separately for each platform', 'slower development cycle', 'JIT-compiled and interpreted languages (Java, Python, JavaScript) are fast enough for most apps'], 'Compiled languages suit performance-critical or distributed binaries; many commercial systems successfully use interpreted or bytecode languages.')],
    extended=[('A team in Bangalore is building a data-analysis tool that must run on Windows, macOS and Linux and be updated weekly. Compare compiling, interpreting and using bytecode with a virtual machine for this product, and recommend an approach.', 'Compiled: fastest, source hidden, but three builds per release and testing on each platform. Interpreted: one source runs everywhere with the interpreter installed, quick updates, slower, source visible. Bytecode/VM (Java/JVM, Python): compile once to platform-independent bytecode, run on any VM, JIT gives near-native speed. Recommend bytecode/VM: portability with good performance and weekly updates.', 6)],
))


@R.add('ch04-st1', 'C3', (2, 5), 'short')
def error_report(rng, slot):
    n = rng.randint(6, 9)
    vals = [rng.randint(1, 9) for _ in range(n)]
    syn = sorted(rng.sample(range(2, n + 1), 2 if slot.d >= 3 else 1))
    lines = []
    for i in range(1, n + 1):
        if i in syn:
            lines.append(f'{i}  print("Total" {vals[i - 1]})' if rng.random() < 0.5 else f'{i}  x = ({vals[i - 1]} + 2')
        else:
            lines.append(f'{i}  print({vals[i - 1]} * 2)')
    out_before = [str(vals[i - 1] * 2) for i in range(1, syn[0])]
    stem = ('The numbered program below contains syntax error(s).\n' + '\n'.join(lines) +
            '\nIdentify the line(s) containing syntax errors, and explain what happens when the program is (a) compiled and (b) run line by line by an interpreter, stating any output produced.')
    ans = (f'(a) The compiler analyses the whole program, reports syntax errors on line(s) {", ".join(map(str, syn))} and produces no executable, so nothing is output. '
           f'(b) The interpreter executes lines 1-{syn[0] - 1}, printing {", ".join(out_before) if out_before else "nothing"}, then stops with a syntax error at line {syn[0]}.')
    return dict(stem=stem, answer=ans, markingKey=ans + ' 2 marks for each part. (Note: CPython parses a whole file first; the answer assumes a line-by-line interpreter as described in the IB guide.)', marks=4)


@R.add('ch04-st1', 'C3', (2, 5), 'numerical')
def compile_vs_interp(rng, slot):
    comp = rng.choice([20, 45, 90, 120])
    rc = rng.choice([0.5, 1, 2])
    ri = rc * rng.choice([5, 10, 20, 30])
    runs = rng.choice([3, 5, 10, 50])
    tc, ti = comp + rc * runs, ri * runs
    be = comp / (ri - rc)
    return dict(stem=f'Compiling a program takes {comp} s and the executable then runs in {rc} s. Interpreting the same program takes {ri} s per run. Calculate the total time for {runs} runs with each approach and the number of runs after which compiling becomes faster.',
                answer=f'Compiled {r2(tc)} s, interpreted {r2(ti)} s; compiling is faster after more than {r2(be, 2)} runs (i.e. from run {math.floor(be) + 1})',
                markingKey=f'Compiled = {comp} + {rc}×{runs} = {r2(tc)} (A1); interpreted = {ri}×{runs} = {r2(ti)} (A1); break-even {comp} + {rc}n = {ri}n → n = {r2(be, 2)} (M1 A1).', marks=4)


@R.add('ch04-st1', 'C3', (1, 4), 'short')
def translator_choice(rng, slot):
    items = [('a beginner learning to program in a classroom', 'interpreter', 'immediate feedback and errors shown at the line where they occur'),
             ('a games company releasing a high-performance PC game', 'compiler', 'fastest execution and the source code is not given away'),
             ('firmware for a microwave oven written in assembly language', 'assembler', 'assembly mnemonics must be converted to the controller\'s machine code'),
             ('a website script that must run in every browser', 'interpreter (with JIT) in the browser', 'the same source runs on any platform\'s browser'),
             ('a scientific simulation run thousands of times', 'compiler', 'translation cost is paid once and optimised code runs fastest each time'),
             ('a system administrator automating small tasks', 'interpreter (scripting language)', 'quick to write and change without recompiling')]
    who, tr, why = rng.choice(items)
    return dict(stem=f'Recommend a type of translator for {who}, and justify your choice.', answer=f'{tr}: {why}.',
                markingKey=f'1 mark for {tr}; 1-2 marks for justification: {why}.', marks=3)


K.ar('ch04-st1', [
    ('Interpreted programs usually run more slowly than compiled programs.', 'An interpreter must translate each statement every time it is executed.', 0, 'Both true; repeated translation is the reason.'),
    ('A compiler is needed every time a compiled program runs.', 'A compiler produces machine code.', 3, 'A false – the executable runs without the compiler; R true.'),
    ('Assembly language must be translated before it can be executed.', 'Assembly programs are usually longer than equivalent high-level programs.', 1, 'Both true, but program length is not the reason; the CPU can only execute machine code.'),
])


R.facts('ch04-st2', F(
    terms=[('lexical analysis', 'the first stage of compilation, in which the source code is broken into tokens and whitespace and comments are removed'),
           ('token', 'a meaningful unit of source code, such as a keyword, identifier, operator, literal or punctuation symbol'),
           ('symbol table', 'a data structure built by the compiler that records each identifier with its type, scope and memory location'),
           ('syntax analysis (parsing)', 'the stage in which the token stream is checked against the grammar of the language and a parse/abstract syntax tree is built'),
           ('semantic analysis', 'checking that a syntactically correct program makes sense, e.g. type compatibility and that variables are declared before use'),
           ('code generation', 'the stage in which the compiler produces object (machine) code from the intermediate representation'),
           ('code optimisation', 'transforming the program so that it runs faster or uses less memory without changing its behaviour, e.g. constant folding or removing dead code')],
    facts=[('In which stage of compilation are comments removed?', 'Lexical analysis', ['Syntax analysis', 'Code generation', 'Optimisation'], 'The lexer discards whitespace and comments while producing tokens.'),
           ('A missing closing bracket is detected during…', 'syntax analysis', ['lexical analysis', 'code generation', 'linking'], 'The token sequence does not match the grammar.'),
           ('Adding a string to an integer in a statically typed language is detected during…', 'semantic analysis', ['lexical analysis', 'optimisation', 'loading'], 'The types are incompatible even though the syntax is valid.'),
           ('Replacing x = 60 * 60 * 24 with x = 86400 at compile time is an example of…', 'constant folding (optimisation)', ['lexical analysis', 'linking', 'interpretation'], 'The compiler evaluates constant expressions in advance.')],
    why=[('Explain why the compiler builds a symbol table.', 'Later stages need to know each identifier\'s type, scope and address – to check declarations and type compatibility (semantic analysis) and to generate the correct memory references (code generation).'),
         ('Explain why code optimisation must not change the output of a program.', 'Optimisation is meant to improve speed or memory use only; the optimised program must be semantically equivalent, otherwise it would introduce bugs the programmer did not write.'),
         ('Explain why lexical analysis happens before syntax analysis.', 'The parser works on tokens; the lexer first groups characters into tokens (identifiers, keywords, numbers), so the grammar can be checked on these meaningful units rather than individual characters.')],
    contrast=[('lexical analysis', 'syntax analysis', 'Lexical analysis converts characters into tokens and spots invalid symbols; syntax analysis checks that the sequence of tokens follows the grammar rules and builds a parse tree.'),
              ('syntax errors', 'semantic errors', 'A syntax error breaks the grammar (e.g. missing bracket); a semantic error is grammatically valid but meaningless, e.g. using an undeclared variable or mismatched types.')],
    misc=[('Lexical analysis checks whether the program is grammatically correct.', 'The lexer only splits the code into tokens; grammar checking is done in syntax analysis.'),
          ('Optimisation is the first stage of compilation.', 'Optimisation works on an intermediate representation after analysis, before or during code generation.'),
          ('The symbol table stores the values of variables while the program runs.', 'The symbol table is a compile-time structure holding names, types, scope and addresses, not run-time values.')],
    evaluate=[('Aggressive compiler optimisation is always desirable.', ['faster, smaller programs', 'programmers can write clear code and let the compiler optimise'], ['longer compile times', 'optimised code is harder to debug (variables removed, code reordered)', 'compiler bugs or undefined behaviour can produce surprising results'], 'Useful for release builds, but debugging builds usually use little optimisation.')],
    extended=[('Describe what happens at each stage of compilation (lexical analysis, syntax analysis, semantic analysis, optimisation, code generation) when the statement total = price * 3 + tax is compiled.', 'Lexical: tokens total (identifier), = (operator), price (identifier), * (operator), 3 (integer literal), + (operator), tax (identifier); symbol-table entries. Syntax: tokens checked against assignment-expression grammar, parse tree built with * before +. Semantic: total, price, tax declared and types compatible. Optimisation: e.g. keep price in a register, constant folding if possible. Code generation: machine code such as LOAD price; MUL #3; ADD tax; STORE total.', 6)],
))

import io as _io
import keyword as _kw
import tokenize as _tok

_STMTS = ['total = price * 3 + tax', 'if score >= 50: print("pass")', 'for i in range(10): count += i', 'area = 3.14 * r ** 2',
          'while n > 0: n = n // 2', 'name = first + " " + last', 'average = sum(marks) / len(marks)', 'if x != y and z < 10: flag = True',
          'result = (a + b) * (c - 4)', 'return value % 7 == 0', 'speed = distance / time', 'items.append(item * 2)']


def _tokens(src):
    out = []
    for t in _tok.generate_tokens(_io.StringIO(src).readline):
        if t.type in (_tok.NEWLINE, _tok.NL, _tok.ENDMARKER, _tok.INDENT, _tok.DEDENT):
            continue
        if t.type == _tok.NAME:
            kind = 'keyword' if _kw.iskeyword(t.string) else 'identifier'
        elif t.type == _tok.NUMBER:
            kind = 'numeric literal'
        elif t.type == _tok.STRING:
            kind = 'string literal'
        elif t.string in '()[]:,.':
            kind = 'punctuation'
        else:
            kind = 'operator'
        out.append((t.string, kind))
    return out


@R.add('ch04-st2', 'C3', (1, 5), 'short')
def lex_tokens(rng, slot):
    s = rng.choice(_STMTS)
    toks = _tokens(s)
    kinds = {}
    for v, k in toks:
        kinds.setdefault(k, []).append(v)
    summ = '; '.join(f'{k}: {" ".join(v)}' for k, v in kinds.items())
    if slot.d <= 2:
        k = rng.choice(list(kinds))
        return dict(stem=f'During lexical analysis the Python statement  {s}  is split into tokens. List the tokens that are {k}s.', answer=' '.join(kinds[k]),
                    markingKey=f'{" ".join(kinds[k])}. All tokens: {summ}.', marks=2)
    return dict(stem=f'During lexical analysis the statement  {s}  is converted into a stream of tokens. State how many tokens are produced and classify each one (keyword, identifier, operator, literal or punctuation).',
                answer=f'{len(toks)} tokens – {summ}', markingKey=f'{len(toks)} tokens (1 mark); classification {summ} (2-3 marks, deduct 1 per error).', marks=4)


def _rpn(expr):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    out, ops = [], []
    for t in expr.split():
        if t in prec:
            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[t]:
                out.append(ops.pop())
            ops.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            while ops[-1] != '(':
                out.append(ops.pop())
            ops.pop()
        else:
            out.append(t)
    while ops:
        out.append(ops.pop())
    return out


def _rand_arith(rng, d):
    vs = rng.sample(['a', 'b', 'c', 'd', 'x', 'y'], 4)
    forms = ['{0} + {1} * {2}', '( {0} + {1} ) * {2}', '{0} * {1} - {2} / {3}', '( {0} - {1} ) * ( {2} + {3} )', '{0} + {1} * {2} - {3}', '{0} / ( {1} + {2} ) * {3}']
    return rng.choice(forms[:3] if d <= 2 else forms).format(*vs)


@R.add('ch04-st2', 'C3', (2, 5), 'short')
def to_postfix(rng, slot):
    e = _rand_arith(rng, slot.d)
    r = ' '.join(_rpn(e))
    vals = {v: rng.randint(1, 9) for v in set(e.split()) if v.isalpha()}
    v = eval(e, {}, vals)
    ask_val = slot.d >= 4
    stem = f'During syntax analysis a compiler converts the infix expression  {e}  into reverse Polish (postfix) notation. Write the postfix form' + (f' and evaluate it with {", ".join(f"{k} = {vals[k]}" for k in sorted(vals))}.' if ask_val else '.')
    ans = r + (f'; value {r2(v, 3)}' if ask_val else '')
    return dict(stem=stem, answer=ans, markingKey=f'{r} (2 marks; operator precedence * / before + −, brackets respected)' + (f'; evaluation using a stack = {r2(v, 3)} (1 mark)' if ask_val else '') + '.', marks=3 if ask_val else 2)


@R.add('ch04-st2', 'C3', (2, 4), 'short')
def const_fold(rng, slot):
    a, b, c = rng.randint(2, 12), rng.randint(2, 12), rng.randint(1, 60)
    forms = [(f'seconds = {a} * 60 * 60 + {c}', a * 3600 + c), (f'size = {a} * 1024 * {b}', a * 1024 * b), (f'area = {a} * {b} * width', None),
             (f'limit = ({a} + {b}) * {c}', (a + b) * c), (f'mask = {2 ** a} - 1', 2 ** a - 1), (f'total = price * ({a} + {b})', None)]
    src, v = rng.choice(forms)
    lhs, rhs = src.split(' = ')
    if v is None:
        folded = rhs.replace(f'{a} * {b}', str(a * b)).replace(f'({a} + {b})', str(a + b))
    else:
        folded = str(v)
    return dict(stem=f'A compiler applies constant folding to the statement  {src}. Write the optimised statement and explain the benefit.',
                answer=f'{lhs} = {folded}', markingKey=f'{lhs} = {folded} (1 mark): the constant part is evaluated once at compile time, so no arithmetic is needed at run time (1 mark); behaviour is unchanged.', marks=2)


K.ar('ch04-st2', [
    ('Comments are removed during lexical analysis.', 'Comments do not affect the meaning of the program.', 0, 'Both true; because they carry no meaning they are discarded.'),
    ('Syntax analysis detects the use of an undeclared variable.', 'Syntax analysis builds a parse tree from the tokens.', 3, 'A false – undeclared variables are found in semantic analysis; R true.'),
    ('Optimisation can remove code that is never executed.', 'Dead code does not change the output of a program.', 0, 'Both true; R explains why removal is safe.'),
])


R.facts('ch04-st3', F(
    terms=[('bytecode', 'an intermediate, platform-independent instruction set produced by compiling source code, designed to be executed by a virtual machine'),
           ('virtual machine (VM)', 'software that emulates a processor, executing bytecode on any real hardware for which the VM has been written'),
           ('just-in-time (JIT) compilation', 'compiling frequently executed bytecode into native machine code at run time so it runs faster'),
           ('Java Virtual Machine (JVM)', 'the virtual machine that runs Java bytecode (.class files) on any platform'),
           ('hot spot', 'a section of code that is executed very often and is therefore worth JIT-compiling'),
           ('ahead-of-time (AOT) compilation', 'compiling a program fully to native code before it is run')],
    facts=[('What is the main advantage of compiling Java to bytecode?', '"Write once, run anywhere" – the same bytecode runs on any device with a JVM', ['Bytecode runs without any software', 'Bytecode is always faster than native code', 'Bytecode cannot be decompiled'], 'Portability is the main aim.'),
           ('Why does a JIT compiler not compile every method immediately?', 'Compiling takes time, so only frequently executed (hot) code is worth compiling', ['JIT compilers cannot compile loops', 'Bytecode cannot be compiled', 'It would use too little memory'], 'Compilation cost must be repaid by faster repeated execution.'),
           ('Which of these uses a virtual machine with bytecode?', 'Java and C# (.NET CLR)', ['Assembly language', 'Hand-written machine code', 'HTML'], 'Both compile to an intermediate language run by a VM.'),
           ('Python source files are automatically compiled to…', 'bytecode (.pyc) that is executed by the Python virtual machine', ['native x86 machine code', 'assembly language', 'Java bytecode'], 'CPython compiles to bytecode and interprets it.')],
    why=[('Explain why JIT compilation can make a program run faster than pure interpretation.', 'Frequently executed code is translated to native machine code once and then executed directly by the CPU, avoiding repeated interpretation; the JIT can also optimise using information gathered at run time.'),
         ('Explain why programs running on a VM may start more slowly than native programs.', 'The VM must load, verify the bytecode and initially interpret it; JIT compilation of hot spots also takes time, so peak speed is reached only after warm-up.'),
         ('Explain why bytecode improves security.', 'The VM can verify bytecode before running it and executes it in a sandbox, checking memory accesses and permissions, so malicious or faulty code cannot directly access the hardware.')],
    contrast=[('bytecode', 'machine code', 'Bytecode is an intermediate, platform-independent instruction set executed by a virtual machine; machine code is binary instructions for a specific physical processor.'),
              ('JIT compilation', 'ahead-of-time compilation', 'JIT compiles bytecode to native code during execution, focusing on hot spots and using run-time information; AOT compiles everything before the program runs, giving fast start-up but no run-time profiling.')],
    misc=[('A Java program needs to be recompiled for every operating system.', 'Java is compiled once to bytecode; each platform supplies its own JVM to run the same bytecode.'),
          ('A virtual machine is the same as an emulator for a games console.', 'A process VM like the JVM runs an abstract bytecode designed for portability, not a copy of real hardware (though both are forms of virtualisation).'),
          ('JIT compilation happens before the program is distributed.', 'JIT compilation happens on the user\'s machine while the program runs.')],
    evaluate=[('Bytecode with a JIT-compiling VM gives the best of both compilation and interpretation.', ['portable like interpreted code', 'near-native speed for hot code', 'sandboxing and verification'], ['slower start-up and warm-up', 'VM uses extra memory', 'peak performance may still trail optimised native code'], 'An excellent compromise for most applications, though real-time or resource-limited systems may prefer AOT native code.')],
    extended=[('A mobile app developer must choose between distributing native machine code for each phone processor and distributing bytecode run by a VM with JIT compilation. Discuss the implications for performance, portability, start-up time, security and battery life.', 'Native: fastest start-up and execution, less memory, but one build per CPU/OS and harder sandboxing. Bytecode + VM: one build for all devices, verification/sandbox, JIT optimises hot code using run-time profiles, but warm-up delay and JIT work use battery and memory. Many platforms (Android ART) combine AOT at install with JIT – a balanced answer with a justified recommendation.', 6)],
))


def _stack_vm(code, env):
    st, trace = [], []
    for ins in code:
        op, *arg = ins.split()
        if op == 'PUSH':
            st.append(int(arg[0]))
        elif op == 'LOAD':
            st.append(env[arg[0]])
        elif op in ('ADD', 'SUB', 'MUL', 'DIV'):
            b, a = st.pop(), st.pop()
            st.append({'ADD': a + b, 'SUB': a - b, 'MUL': a * b, 'DIV': a // b}[op])
        trace.append(list(st))
    return st, trace


@R.add('ch04-st3', 'C3', (2, 5), 'short')
def stack_vm(rng, slot):
    e = _rand_arith(rng, slot.d).replace('/', '*')
    vals = {v: rng.randint(1, 9) for v in set(e.split()) if v.isalpha()}
    code = []
    for t in _rpn(e):
        code.append({'+': 'ADD', '-': 'SUB', '*': 'MUL'}[t] if t in '+-*' else f'LOAD {t}')
    if slot.d >= 4 and rng.random() < 0.5:
        k = rng.randint(2, 5)
        code += [f'PUSH {k}', 'MUL']
    st, trace = _stack_vm(code, vals)
    env_txt = ', '.join(f'{k} = {vals[k]}' for k in sorted(vals))
    return dict(stem=f'A stack-based virtual machine executes this bytecode, where LOAD pushes a variable, PUSH pushes a constant and ADD/SUB/MUL pop two values and push the result (the value popped second is the left operand). With {env_txt}:\n' + '\n'.join(code) + '\nState the value left on the stack and the maximum stack depth reached.',
                answer=f'{st[-1]}; maximum depth {max(len(t) for t in trace)}', markingKey='Stack after each instruction: ' + ' | '.join(' '.join(map(str, t)) for t in trace) + f'. Result {st[-1]} (2 marks), maximum depth {max(len(t) for t in trace)} (1 mark).', marks=3)


@R.add('ch04-st3', 'C3', (2, 5), 'numerical')
def jit_breakeven(rng, slot):
    ti = rng.choice([4, 6, 8, 10])   # microseconds per call interpreted
    tn = rng.choice([0.5, 1, 2])
    cc = rng.choice([200, 500, 1000, 2000])
    calls = rng.choice([50, 100, 300, 1000, 5000])
    be = cc / (ti - tn)
    t_int = ti * calls
    t_jit = cc + tn * calls
    return dict(stem=f'A method takes {ti} µs per call when interpreted by a VM and {tn} µs when JIT-compiled to native code, but compiling it costs {cc} µs. Calculate the total time for {calls} calls with and without JIT compilation, and the minimum number of calls for JIT compilation to pay off.',
                answer=f'Interpreted {r2(t_int)} µs; JIT {r2(t_jit)} µs; pays off after more than {r2(be, 2)} calls',
                markingKey=f'Interpreted {ti}×{calls} = {r2(t_int)} (A1); JIT {cc} + {tn}×{calls} = {r2(t_jit)} (A1); {cc} = ({ti} − {tn})n → n = {r2(be, 2)} (M1 A1). This is why VMs only compile hot spots.', marks=4)


K.ar('ch04-st3', [
    ('Java bytecode can run on different operating systems without recompilation.', 'Each operating system has its own JVM that executes the same bytecode.', 0, 'Both true; R explains A.'),
    ('JIT compilers compile every method as soon as the program starts.', 'JIT compilation produces native machine code.', 3, 'A false – only hot code is compiled; R true.'),
    ('Programs on a VM can be sandboxed.', 'The VM checks bytecode and controls access to system resources.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch05 A2.1/A2.2 Network fundamentals and architecture
# =============================================================================================
R.facts('ch05-st1', F(
    terms=[('LAN (local area network)', 'a network that connects devices within a small geographical area such as a home, school or office, usually using infrastructure owned by the organisation'),
           ('WAN (wide area network)', 'a network that connects devices or LANs over a large geographical area, usually using leased telecommunications links'),
           ('PAN (personal area network)', 'a very small network connecting devices around one person, e.g. a phone, smartwatch and earbuds over Bluetooth'),
           ('VPN (virtual private network)', 'an encrypted connection (tunnel) over a public network such as the internet that lets a remote user or site act as if it were on a private network'),
           ('internet', 'the global network of interconnected networks that communicate using the TCP/IP protocol suite'),
           ('intranet', 'a private network that uses internet technologies but is accessible only to members of an organisation'),
           ('WLAN', 'a wireless local area network, usually using Wi-Fi (IEEE 802.11)')],
    facts=[('Which network type best describes a smartwatch connected to a phone by Bluetooth?', 'PAN', ['LAN', 'WAN', 'MAN'], 'A PAN covers only a few metres around one person.'),
           ('A bank connects branch LANs in five countries using leased lines. This is a…', 'WAN', ['PAN', 'WLAN', 'VLAN'], 'WANs span large geographical areas.'),
           ('What does a VPN mainly provide for a remote worker using hotel Wi-Fi?', 'An encrypted tunnel to the company network', ['Faster internet speed', 'A free IP address', 'Protection against all malware'], 'Traffic is encrypted across the untrusted network.'),
           ('The internet is best described as…', 'a network of networks using TCP/IP', ['the World Wide Web', 'a single very large LAN', 'a company\'s private network'], 'The web is a service running on the internet.')],
    why=[('Explain why a company might use a VPN rather than leased lines to connect a small branch office.', 'A VPN uses the existing internet connection with encryption, so it is much cheaper and quicker to set up than leasing a dedicated line, while still keeping data confidential.'),
         ('Explain why LANs usually have higher data rates than WANs.', 'LANs cover short distances with the organisation\'s own cabling and switches, so there is less attenuation and congestion; WANs use long, shared, leased links that are costly to make high-bandwidth.'),
         ('Explain why the internet and the World Wide Web are not the same thing.', 'The internet is the global infrastructure of connected networks; the web is one service that runs on it (web pages over HTTP), alongside others such as email, VoIP and file transfer.')],
    contrast=[('a LAN', 'a WAN', 'A LAN covers a small area and is usually owned and managed by the organisation, with high speeds; a WAN covers a large area using leased/third-party links, with lower speeds and higher costs.'),
              ('an intranet', 'the internet', 'An intranet is a private network for an organisation\'s members only; the internet is the public, global network of networks.')],
    misc=[('A VPN makes the user completely anonymous and safe from all attacks.', 'A VPN encrypts traffic between the device and the VPN server, but the provider can see traffic and it does not stop malware or phishing.'),
          ('A WAN is just a LAN with more computers.', 'The difference is geographical spread and ownership of links, not the number of devices.'),
          ('Wi-Fi and the internet are the same thing.', 'Wi-Fi is a wireless LAN technology; the internet is the global network that the LAN may connect to through a router.')],
    evaluate=[('All employees should work through a VPN when outside the office.', ['protects confidential data on public Wi-Fi', 'gives secure access to internal systems'], ['adds latency and can slow connections', 'VPN servers become a bottleneck and a target', 'zero-trust approaches may be more appropriate'], 'Generally sensible for accessing internal resources, but should be combined with other controls.')],
    extended=[('A school in Lima has three buildings on one campus, staff who work from home and students with tablets. Recommend the types of network (LAN, WLAN, WAN, VPN) it needs and justify how they would be connected.', 'Wired LAN with switches in each building connected by fibre backbone; WLAN access points for tablets; router/firewall connecting the campus LAN to the internet (WAN link via ISP); VPN for staff working from home to access the school\'s servers securely. Justify with speed, mobility, security and cost.', 6)],
))

_NET_SCEN = [('a phone, smartwatch and wireless earbuds connected via Bluetooth', 'PAN'), ('30 computers and a printer connected by switches in one school building', 'LAN'),
             ('laptops connected to access points in a café', 'WLAN'), ('the offices of a retail chain in Toronto, Vancouver and Montréal linked by leased lines', 'WAN'),
             ('an employee at home securely accessing the company file server over the internet', 'VPN'), ('a university campus network spanning several buildings across a city district', 'MAN / campus network'),
             ('a fitness tracker sending data to a phone in the user\'s pocket', 'PAN'), ('a hospital\'s internal staff portal available only on its own network', 'intranet')]


@R.add('ch05-st1', 'C3', (1, 3), 'short')
def net_type(rng, slot):
    s = rng.sample(_NET_SCEN, 3)
    ans = '; '.join(f'{a} – {b}' for a, b in s)
    return dict(stem='Identify the type of network in each case: ' + '; '.join(f'({chr(97 + i)}) {a}' for i, (a, b) in enumerate(s)) + '.', answer=ans, markingKey=f'1 mark each: {ans}.', marks=3)


@R.add('ch05-st1', 'C3', (2, 5), 'numerical')
def vpn_overhead(rng, slot):
    payload = rng.choice([500, 1000, 1200, 1400])
    hdr = rng.choice([40, 52, 60, 73])
    rate = rng.choice([10, 20, 50, 100])
    size = rng.choice([50, 200, 500])
    pk = math.ceil(size * 1e6 / payload)
    extra = pk * hdr
    eff = payload / (payload + hdr)
    return dict(stem=f'A VPN adds {hdr} bytes of encryption and tunnel headers to every packet that carries {payload} bytes of data. A user sends a {size} MB file (1 MB = 10^6 bytes). Calculate the number of packets, the extra bytes added, and the effective data rate on a {rate} Mbit/s link.',
                answer=f'{pk:,} packets; {extra:,} extra bytes; effective rate ≈ {r2(rate * eff, 2)} Mbit/s',
                markingKey=f'Packets = ⌈{size}×10^6 / {payload}⌉ = {pk:,} (A1); overhead = {pk:,} × {hdr} = {extra:,} B (A1); efficiency = {payload}/{payload + hdr} = {r2(eff, 4)}, × {rate} = {r2(rate * eff, 2)} Mbit/s (M1 A1).', marks=4)


K.ar('ch05-st1', [
    ('A VPN protects data sent over public Wi-Fi.', 'A VPN encrypts traffic between the device and the VPN server.', 0, 'Both true; encryption is why.'),
    ('The World Wide Web is the same as the internet.', 'Web pages are transferred using HTTP over the internet.', 3, 'A false – the web is a service on the internet; R true.'),
    ('A LAN is usually faster than a WAN.', 'LANs cover a smaller geographical area with the organisation\'s own cabling.', 0, 'Both true; R explains A.'),
])


R.facts('ch05-st2', F(
    terms=[('router', 'a device that forwards packets between different networks using IP addresses and routing tables'),
           ('switch', 'a device that connects devices within a LAN and forwards frames only to the port of the destination MAC address'),
           ('wireless access point (WAP)', 'a device that allows wireless devices to connect to a wired network'),
           ('network interface controller (NIC)', 'the hardware in a device that connects it to a network and has a unique MAC address'),
           ('modem', 'a device that converts digital data into signals suitable for a transmission medium such as a telephone or cable line, and back again'),
           ('MAC address', 'a 48-bit hardware address assigned to a network interface, usually written as six pairs of hexadecimal digits'),
           ('hub', 'a simple device that repeats every incoming frame to all other ports')],
    facts=[('Which device forwards data between a home network and the internet?', 'Router', ['Switch', 'Hub', 'NIC'], 'Routers connect different networks.'),
           ('Which address does a switch use to forward frames?', 'MAC address', ['IP address', 'URL', 'Port number'], 'Switches work at the data-link layer.'),
           ('Why is a switch more efficient than a hub?', 'It sends frames only to the destination port instead of every port', ['It has more ports', 'It converts analogue to digital', 'It assigns IP addresses'], 'Less unnecessary traffic and fewer collisions.'),
           ('A MAC address is how many bits long?', '48', ['32', '64', '128'], 'Six bytes written as 12 hex digits.')],
    why=[('Explain why a switch reduces network congestion compared with a hub.', 'The switch learns which MAC address is on each port and forwards each frame only to the destination port, so other links are not filled with traffic and several pairs can communicate at once; a hub broadcasts every frame to every port.'),
         ('Explain why every device needs a NIC to join a network.', 'The NIC provides the physical connection (cable socket or radio), converts data into signals for the medium, and has a unique MAC address so frames can be delivered to that device.'),
         ('Explain why a home "router" is actually several devices in one box.', 'It combines a router (forwards between home LAN and ISP), a switch (wired ports), a wireless access point (Wi-Fi), a modem (converts signals for the line) and often a firewall and DHCP server, which saves cost and space.')],
    contrast=[('a router', 'a switch', 'A router forwards packets between different networks using IP addresses; a switch forwards frames between devices on the same LAN using MAC addresses.'),
              ('a MAC address', 'an IP address', 'A MAC address is a fixed hardware address of a NIC used for delivery on the local network; an IP address is a logical address, which can change, used to route data between networks.')],
    misc=[('A switch uses IP addresses to decide where to send data.', 'A (layer-2) switch uses MAC addresses; routers use IP addresses.'),
          ('A wireless access point connects a home network to the internet.', 'A WAP lets wireless devices join a LAN; a router/modem provides the internet connection.'),
          ('MAC addresses change every time a device connects to a new network.', 'The MAC address is assigned to the NIC by the manufacturer (though some devices randomise it for privacy); IP addresses are the ones that usually change.')],
    evaluate=[('A business should replace all wired connections with Wi-Fi.', ['mobility and no cabling cost', 'easy to add devices'], ['lower and more variable speeds; interference', 'security risks from wireless eavesdropping', 'servers and desktops benefit from wired reliability'], 'Wi-Fi should complement, not replace, wired connections for fixed, high-traffic devices.')],
    extended=[('A small architecture firm in Dubai has 15 desktop PCs, a file server, two printers, guest Wi-Fi and a fibre internet connection. Describe the network devices it needs and explain the role of each, including how guest traffic is kept separate.', 'Switch(es) connecting PCs, server and printers by cable; wireless access points for laptops/guests; router connecting LAN to ISP (with modem/ONT for fibre); firewall to filter traffic; NICs in every device. Guest Wi-Fi on a separate SSID/VLAN with its own subnet so guests reach only the internet; DHCP assigns addresses.', 6)],
))


@R.add('ch05-st2', 'C3', (2, 5), 'short')
def switch_learn(rng, slot):
    hosts = rng.sample(['A', 'B', 'C', 'D', 'E'], 4)
    port = {h: i + 1 for i, h in enumerate(hosts)}
    nf = 3 if slot.d <= 3 else 5
    frames = []
    for _ in range(nf):
        s, d = rng.sample(hosts, 2)
        frames.append((s, d))
    table_, res = {}, []
    for s, d in frames:
        table_[s] = port[s]
        if d in table_:
            res.append(f'{s}→{d}: forwarded only to port {table_[d]}')
        else:
            res.append(f'{s}→{d}: flooded to all ports except {port[s]}')
    conn = ', '.join(f'{h} on port {port[h]}' for h in hosts)
    final = ', '.join(f'{h}: port {p}' for h, p in sorted(table_.items()))
    return dict(stem=f'A switch has an empty MAC address table. Hosts are connected as follows: {conn}. These frames are sent in order: {", ".join(f"{s} to {d}" for s, d in frames)}. For each frame state whether the switch floods it or forwards it to a single port, and give the final MAC table.',
                answer='; '.join(res) + f'. Final table: {final}', markingKey='The switch records the source MAC/port of every frame; unknown destinations are flooded. ' + '; '.join(res) + f'. Final table {final}. 1 mark per frame, 1 for the table.', marks=nf + 1)


@R.add('ch05-st2', 'C3', (1, 3), 'short')
def device_for(rng, slot):
    items = [('connect 24 wired PCs in one office so they can share files', 'switch'), ('connect the office network to the ISP and the internet', 'router'),
             ('let laptops and phones join the wired LAN without cables', 'wireless access point'), ('convert digital data to signals for a DSL telephone line', 'modem'),
             ('give a desktop computer a physical network connection with a MAC address', 'NIC'), ('block incoming traffic that does not match the security rules', 'firewall'),
             ('extend a cable run beyond 100 m by regenerating the signal', 'repeater')]
    s = rng.sample(items, 3)
    ans = '; '.join(f'{a} – {b}' for a, b in s)
    return dict(stem='State the network device that is needed to: ' + '; '.join(f'({chr(97 + i)}) {a}' for i, (a, b) in enumerate(s)) + '.', answer=ans, markingKey=f'1 mark each: {ans}.', marks=3)


@R.add('ch05-st2', 'C1', (1, 3), 'mcq')
def mac_mcq(rng, slot):
    mac = ':'.join(f'{rng.randint(0, 255):02X}' for _ in range(6))
    oui = ':'.join(mac.split(':')[:3])
    return nmcq(rng, f'A NIC has the MAC address {mac}. Which part identifies the manufacturer (OUI)?', oui,
                [':'.join(mac.split(':')[3:]), mac.split(':')[0], ':'.join(mac.split(':')[2:5])], 'The first 24 bits (3 bytes) are the organisationally unique identifier.')


K.ar('ch05-st2', [
    ('A router connects different networks.', 'Routers forward packets using IP addresses and routing tables.', 0, 'Both true; R explains how A works.'),
    ('A hub sends each frame only to its destination.', 'A hub does not read MAC addresses.', 3, 'A false – a hub broadcasts to all ports; R true.'),
    ('A switch learns MAC addresses automatically.', 'A switch records the source MAC address and port of each frame it receives.', 0, 'Both true; R explains A.'),
])


R.facts('ch05-st3', F(
    terms=[('network topology', 'the arrangement of nodes and the links between them in a network, either physical (cabling) or logical (data flow)'),
           ('star topology', 'a topology in which every node is connected to a central switch or hub'),
           ('bus topology', 'a topology in which all nodes share a single backbone cable with terminators at each end'),
           ('ring topology', 'a topology in which each node is connected to exactly two others, forming a closed loop through which data passes'),
           ('mesh topology', 'a topology in which nodes have multiple connections to other nodes; in a full mesh every node connects to every other'),
           ('single point of failure', 'a component whose failure stops the whole network or system from working'),
           ('hybrid topology', 'a combination of two or more topologies, such as several stars connected by a bus or mesh backbone')],
    facts=[('How many links are needed for a full mesh of 6 nodes?', '15', ['6', '12', '30'], 'n(n − 1)/2 = 6 × 5 / 2 = 15.'),
           ('In a star network, what happens if the central switch fails?', 'All nodes lose connection to each other', ['Only one node is affected', 'Data is rerouted around the ring', 'Nothing – each node has a backup link'], 'The central device is a single point of failure.'),
           ('Which topology is used by the core of the internet?', 'Partial mesh', ['Bus', 'Ring', 'Star'], 'Multiple redundant paths between routers.'),
           ('In a bus topology, what happens when two nodes transmit simultaneously?', 'A collision occurs and both must retransmit', ['The faster node wins', 'Data is merged', 'The terminator stores the data'], 'The shared medium carries one signal at a time.')],
    why=[('Explain why the star topology is the most common in modern LANs.', 'Each device has its own cable to the switch, so a cable fault affects only that device, devices are easy to add, and the switch sends frames only where needed, giving good performance; the cost is extra cabling and the switch as a single point of failure.'),
         ('Explain why a full mesh is rarely used to connect many devices.', 'The number of links grows as n(n − 1)/2, so cabling, ports and cost grow very quickly; partial meshes give enough redundancy at much lower cost.'),
         ('Explain why a mesh topology is more reliable than a bus.', 'Mesh has multiple paths between nodes, so traffic can be rerouted around a failed link or node; in a bus a single break in the backbone splits or stops the network.')],
    contrast=[('a star topology', 'a mesh topology', 'In a star all nodes connect to one central device (cheap, simple, but single point of failure); in a mesh nodes have multiple direct links (redundant, reliable, but many links and high cost).'),
              ('a physical topology', 'a logical topology', 'The physical topology is how devices are actually cabled; the logical topology is how data flows between them, e.g. physically a star but logically a bus with a hub.')],
    misc=[('In a star topology, if one computer\'s cable is cut, the whole network fails.', 'Only that computer loses its connection; the others still communicate through the switch.'),
          ('A full mesh of n nodes needs n links.', 'A full mesh needs n(n − 1)/2 links because every pair of nodes is connected.'),
          ('A ring topology has no single point of failure.', 'In a simple (single) ring, one broken link or node can stop data circulating; dual rings are needed for resilience.')],
    evaluate=[('A mesh topology is the best choice for a school network.', ['high reliability and redundancy'], ['very expensive cabling and ports', 'complex to configure', 'school traffic does not need that redundancy'], 'A star (or extended star with a small redundant core) is more appropriate for a school; mesh suits critical backbones.')],
    extended=[('A factory has 4 production halls, each with 20 machines. Compare a star in each hall connected by a bus backbone with a star in each hall connected by a mesh of core switches, calculating the number of backbone links for the mesh and discussing reliability, cost and performance.', 'Mesh of 4 core switches = 4×3/2 = 6 links vs 3 segments on the bus. Mesh: any single backbone failure is bypassed, higher aggregate bandwidth, but more cost and configuration. Bus: cheap but a single break splits halls and the backbone is a bottleneck. Hybrid star-mesh recommended for a factory where downtime is costly.', 6)],
))


def _reachable(adj, start, dead_nodes=(), dead_links=()):
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v in dead_nodes or frozenset((u, v)) in dead_links or v in seen:
                continue
            seen.add(v); q.append(v)
    return seen


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def topo_links(rng, slot):
    n = rng.randint(4, 12) + (slot.d - 1) * 3
    kind = rng.choice(['mesh', 'star', 'ring', 'compare'])
    if kind == 'mesh':
        return dict(stem=f'Calculate the number of links needed to connect {n} nodes in a full mesh, and the number of network ports each node needs.', answer=f'{n * (n - 1) // 2} links; {n - 1} ports per node',
                    markingKey=f'n(n − 1)/2 = {n}×{n - 1}/2 = {n * (n - 1) // 2} (M1 A1); each node links to {n - 1} others (A1).', marks=3)
    if kind == 'star':
        return dict(stem=f'{n} computers are connected in a star around one switch. State the number of cables needed and the minimum number of switch ports, and how many computers lose connectivity if (a) one cable fails (b) the switch fails.', answer=f'{n} cables; {n} ports; (a) 1 (b) all {n}',
                    markingKey=f'{n} cables, {n} ports (1 mark each); (a) only the computer on that cable; (b) all {n} – single point of failure (1 mark each).', marks=4)
    if kind == 'ring':
        return dict(stem=f'{n} nodes form a bidirectional ring. State the number of links and the maximum number of hops between any two nodes, and explain the effect of one link failing.', answer=f'{n} links; max {n // 2} hops; after one failure the ring becomes a line, so all nodes stay connected but the maximum distance rises to {n - 1} hops',
                    markingKey=f'{n} links (1); ⌊{n}/2⌋ = {n // 2} hops (1); one failure – data can still go the other way, worst case {n - 1} hops (2).', marks=4)
    return dict(stem=f'Compare the total number of links required for {n} nodes connected as a star (including the central switch as a node), a ring and a full mesh.', answer=f'Star {n}, ring {n}, full mesh {n * (n - 1) // 2}',
                markingKey=f'Star {n} (1), ring {n} (1), mesh {n}×{n - 1}/2 = {n * (n - 1) // 2} (1).', marks=3)


@R.add('ch05-st3', 'C3', (3, 5), 'short')
def topo_fail(rng, slot):
    nodes = list('ABCDEFG')[:rng.randint(5, 7)]
    edges = set()
    for i in range(1, len(nodes)):
        edges.add(frozenset((nodes[i], rng.choice(nodes[:i]))))
    for _ in range(rng.randint(1, 3)):
        a, b = rng.sample(nodes, 2)
        edges.add(frozenset((a, b)))
    adj = {n: [] for n in nodes}
    for e in edges:
        a, b = sorted(e)
        adj[a].append(b); adj[b].append(a)
    failed = rng.choice(nodes[1:])
    src = nodes[0]
    reach = _reachable(adj, src, dead_nodes={failed})
    cut = sorted(set(nodes) - reach - {failed})
    links = ', '.join(sorted('-'.join(sorted(e)) for e in edges))
    return dict(stem=f'A partial-mesh network has the links {links}. Node {failed} fails. List the nodes that node {src} can still reach and the nodes that are cut off from {src}.',
                answer=f'Reachable: {", ".join(sorted(reach - {src})) or "none"}; cut off: {", ".join(cut) or "none"}',
                markingKey=f'Remove {failed} and its links, then follow remaining links from {src}: reachable {", ".join(sorted(reach - {src})) or "none"}; cut off {", ".join(cut) or "none"} (1 mark each). A further mark for noting the redundant paths (or single points of failure).', marks=3)


K.ar('ch05-st3', [
    ('A full mesh is highly fault tolerant.', 'Every node has a direct link to every other node.', 0, 'Both true; R explains A.'),
    ('In a star network the switch is a single point of failure.', 'All traffic between nodes passes through the central switch.', 0, 'Both true; R explains A.'),
    ('A bus network needs n(n − 1)/2 cables.', 'All nodes in a bus share one backbone cable.', 3, 'A false (one backbone plus drop cables); R true.'),
])


R.facts('ch05-st4', F(
    terms=[('client-server model', 'a network model in which central servers provide services or resources that client devices request'),
           ('peer-to-peer (P2P) network', 'a network in which every node can act as both client and server, sharing resources directly with other peers'),
           ('server', 'a computer or program that provides a service, such as files, web pages or email, to clients on request'),
           ('client', 'a device or program that requests services from a server'),
           ('seeder', 'in a P2P file-sharing network, a peer that has the complete file and uploads it to others'),
           ('scalability', 'the ability of a system to handle growing numbers of users or amounts of work by adding resources')],
    facts=[('Which is an advantage of a client-server network?', 'Centralised backups, security and user management', ['No single point of failure', 'No need for any server hardware', 'Every peer contributes upload bandwidth'], 'Central control is the main advantage.'),
           ('In a BitTorrent swarm, why does the download often get faster as more users join?', 'Each new peer also uploads pieces to others, adding capacity', ['The tracker increases its bandwidth', 'Files become smaller', 'Servers are added automatically'], 'P2P capacity grows with the number of peers.'),
           ('Which service is usually provided using the client-server model?', 'Online banking', ['Blockchain consensus', 'BitTorrent file sharing', 'Ad hoc file sharing between two laptops'], 'Banks need central control and security.'),
           ('A home network where each PC shares its own printer and folders without a server is…', 'peer-to-peer', ['client-server', 'thin-client', 'cloud SaaS'], 'Each node shares its resources directly.')],
    why=[('Explain why a client-server network is easier to secure than a peer-to-peer network.', 'Data and permissions are managed centrally on the server, so one administrator can enforce authentication, access rights, updates and backups; in P2P each peer controls its own resources and security varies.'),
         ('Explain why a P2P network can scale better than a single server for distributing a popular file.', 'In P2P every downloader also uploads pieces to others, so total upload capacity grows with the number of peers; a single server\'s upload bandwidth is fixed and is shared among more and more clients.'),
         ('Explain why a server is a potential single point of failure.', 'All clients depend on it for the service; if it crashes or is attacked, the service is unavailable to everyone unless there is redundancy such as backup or load-balanced servers.')],
    contrast=[('client-server', 'peer-to-peer', 'In client-server, dedicated servers provide services that clients request, with central management; in P2P all nodes are equal and share resources directly, with no central control.')],
    misc=[('P2P networks are only used for illegal file sharing.', 'P2P is used legitimately for software updates (e.g. game patches), blockchain, video calls and content distribution.'),
          ('In client-server networks, clients cannot store any data locally.', 'Clients can store data locally; the model only means that shared services are provided by servers.'),
          ('Adding more clients to a client-server system never affects performance.', 'Each extra client adds load to the server; without scaling, response times get worse.')],
    evaluate=[('Peer-to-peer networks are better than client-server networks for a small office of five people.', ['cheap – no dedicated server', 'easy to set up'], ['no central backups or security', 'files spread over many PCs', 'performance suffers if a PC is in use or switched off'], 'P2P may suffice for very small offices with low security needs, but a small server or cloud service is better once data matters.')],
    extended=[('A game company must distribute a 40 GB update to 2 million players. Compare distributing it from its own servers (client-server) with a P2P approach, considering speed, cost, reliability and security.', 'Client-server: easy to control and verify, but needs huge bandwidth (80 PB) and expensive CDN capacity; downloads slow at launch peaks. P2P: players share pieces, so capacity scales with demand and cost falls, but uses players\' upload bandwidth, needs integrity checks (hashes/signatures) to prevent tampering, and may be blocked by some networks. A hybrid (CDN plus P2P) is common.', 6)],
))


@R.add('ch05-st4', 'C3', (2, 5), 'numerical')
def p2p_time(rng, slot):
    F_ = rng.choice([1, 2, 4, 8])      # Gbit
    us = rng.choice([100, 200, 500, 1000])  # Mbit/s server upload
    d = rng.choice([10, 20, 50])       # Mbit/s per peer download
    u = rng.choice([1, 2, 5])          # Mbit/s per peer upload
    N = rng.choice([10, 100, 1000])
    Fm = F_ * 1000
    cs = max(N * Fm / us, Fm / d)
    p2p = max(Fm / us, Fm / d, N * Fm / (us + N * u))
    return dict(stem=f'A {F_} Gbit file (1 Gbit = 1000 Mbit) must reach {N} users. The server uploads at {us} Mbit/s; each user downloads at {d} Mbit/s and uploads at {u} Mbit/s. Using the minimum distribution time formulas D_cs = max(NF/u_s, F/d) and D_p2p = max(F/u_s, F/d, NF/(u_s + N·u)), calculate both times.',
                answer=f'Client-server {r2(cs, 1)} s; P2P {r2(p2p, 1)} s', markingKey=f'D_cs = max({N}×{Fm}/{us}, {Fm}/{d}) = {r2(cs, 1)} s (M1 A1); D_p2p = max({Fm}/{us}, {Fm}/{d}, {N}×{Fm}/({us} + {N}×{u})) = {r2(p2p, 1)} s (M1 A1).', marks=4)


@R.add('ch05-st4', 'C3', (1, 4), 'short')
def model_choice(rng, slot):
    items = [('a hospital storing confidential patient records for 400 staff', 'client-server', 'central security, access control, backups and auditing are essential'),
             ('two friends sharing holiday photos directly between laptops', 'peer-to-peer', 'no server is needed for a small, temporary, low-security exchange'),
             ('a cryptocurrency that must not depend on any single organisation', 'peer-to-peer', 'there is no central authority; every node holds a copy of the ledger'),
             ('a school with shared network drives and student log-ins', 'client-server', 'central user accounts, file storage and backups can be managed by IT staff'),
             ('an open-source project distributing a 6 GB Linux image', 'peer-to-peer (BitTorrent) alongside mirrors', 'peers share upload bandwidth so demand peaks are handled cheaply'),
             ('an online multiplayer game with competitive rankings', 'client-server', 'an authoritative server prevents cheating and keeps a consistent game state')]
    who, m, why = rng.choice(items)
    return dict(stem=f'Recommend whether a client-server or peer-to-peer model should be used for {who}, justifying your answer.', answer=f'{m}: {why}.',
                markingKey=f'{m} (1); justification: {why} (1-2).', marks=3)


K.ar('ch05-st4', [
    ('P2P networks have no single point of failure for the data.', 'Copies of data are held by many peers.', 0, 'Both true; R explains A.'),
    ('Client-server networks are easier to back up.', 'Data is stored centrally on servers.', 0, 'Both true; R explains A.'),
    ('In a P2P network one peer controls the access rights of all the others.', 'P2P peers can act as both clients and servers.', 3, 'A false – there is no central control; R true.'),
])


R.facts('ch05-st5', F(
    terms=[('subnetting', 'dividing a single IP network into smaller logical networks (subnets) by borrowing bits from the host part of the address'),
           ('subnet mask', 'a 32-bit value that marks which bits of an IPv4 address are the network part (1s) and which are the host part (0s)'),
           ('CIDR notation', 'writing a network as an address followed by a slash and the number of network bits, e.g. 192.168.1.0/24'),
           ('network address', 'the first address of a subnet, with all host bits 0, which identifies the subnet itself'),
           ('broadcast address', 'the last address of a subnet, with all host bits 1, used to send to every host in the subnet'),
           ('network segmentation', 'splitting a network into separate segments or subnets (physically or with VLANs) to improve performance and security'),
           ('VLAN', 'a virtual LAN: a logical group of switch ports that behaves as a separate network regardless of physical location')],
    facts=[('How many usable host addresses are there in a /26 subnet?', '62', ['64', '26', '30'], '2^(32−26) − 2 = 64 − 2 = 62.'),
           ('Which subnet mask corresponds to /20?', '255.255.240.0', ['255.255.255.0', '255.255.248.0', '255.240.0.0'], '20 ones: 8+8+4 → third octet 11110000 = 240.'),
           ('Why does segmenting a network improve performance?', 'Broadcast traffic is confined to each segment', ['It increases cable speed', 'It removes the need for routers', 'It gives every device a public IP address'], 'Smaller broadcast domains mean less unnecessary traffic.'),
           ('Two hosts on different subnets need which device to communicate?', 'A router (or layer-3 switch)', ['A hub', 'A repeater', 'A modem only'], 'Traffic between subnets must be routed.')],
    why=[('Explain why network segmentation improves security.', 'Sensitive systems (e.g. servers, payment terminals) can be placed in separate subnets/VLANs with firewall rules between them, so an attacker who compromises one segment cannot easily reach others, and access can be restricted by role.'),
         ('Explain why two addresses in each subnet cannot be assigned to hosts.', 'The address with all host bits 0 identifies the network itself and the address with all host bits 1 is the broadcast address, so neither can identify an individual host.'),
         ('Explain why a network administrator might use VLANs rather than separate physical switches.', 'VLANs create logically separate networks on the same switch hardware, so groups (staff, students, guests) can be separated without extra cabling or devices, and membership can be changed in software.')],
    contrast=[('a subnet mask', 'an IP address', 'An IP address identifies a host interface; the subnet mask shows which bits of that address are the network part and which are the host part.'),
              ('a network address', 'a broadcast address', 'The network address (all host bits 0) identifies the subnet; the broadcast address (all host bits 1) delivers a packet to every host in the subnet.')],
    misc=[('A /24 network has 256 usable host addresses.', 'A /24 has 256 addresses but 254 usable hosts, because the network and broadcast addresses are reserved.'),
          ('Subnetting increases the total number of IP addresses an organisation owns.', 'Subnetting divides an existing address block; it adds network and broadcast addresses per subnet, so usable hosts decrease slightly.'),
          ('Devices in different VLANs on the same switch can always talk directly.', 'VLANs are separate broadcast domains; traffic between them must pass through a router or layer-3 switch.')],
    evaluate=[('Every organisation should segment its network into many small subnets.', ['contains attacks and broadcast traffic', 'allows role-based firewall rules'], ['more complex to configure and troubleshoot', 'needs routing between segments, adding cost', 'too many subnets can waste addresses'], 'Segmentation by function and security level is good practice; the number of segments should match the organisation\'s size and risk.')],
    extended=[('A college has the network 172.16.8.0/22 and needs separate subnets for 300 students, 120 staff, 50 servers and 20 guest devices. Design a subnet plan using variable-length subnet masks, giving each subnet\'s network address, prefix and usable host range.', 'Students 300 hosts → /23 (510): 172.16.8.0/23, hosts .8.1-.9.254; staff 120 → /25 (126): 172.16.10.0/25, .10.1-.10.126; servers 50 → /26 (62): 172.16.10.128/26, .129-.190; guests 20 → /27 (30): 172.16.10.192/27, .193-.222. Remaining space 172.16.10.224/27 and 172.16.11.0/24 kept for growth. Allocate largest first to avoid overlap.', 6)],
))


@R.add('ch05-st5', 'C3', (1, 5), 'short')
def subnet_info(rng, slot):
    pre = rng.choice([24, 25, 26, 27, 28, 29, 30] if slot.d <= 3 else [19, 20, 21, 22, 23, 26, 27, 28, 29])
    base = rng.choice(['10', '172.16', '192.168'])
    parts = base.split('.')
    while len(parts) < 4:
        parts.append(str(rng.randint(0, 255)))
    ip = ipaddress.ip_interface('.'.join(parts) + f'/{pre}')
    net = ip.network
    hosts = net.num_addresses - 2
    first, last = net.network_address + 1, net.broadcast_address - 1
    return dict(stem=f'A host has the IP address {ip.ip} with the subnet mask {net.netmask} (/{pre}). Determine the network address, the broadcast address, the range of usable host addresses and the number of usable hosts.',
                answer=f'Network {net.network_address}; broadcast {net.broadcast_address}; hosts {first} – {last}; {hosts} usable hosts',
                markingKey=f'Host bits = 32 − {pre} = {32 - pre}; AND address with mask → network {net.network_address} (A1); set host bits to 1 → broadcast {net.broadcast_address} (A1); range {first}-{last} (A1); 2^{32 - pre} − 2 = {hosts} (A1).', marks=4)


@R.add('ch05-st5', 'C3', (2, 5), 'short')
def subnet_split(rng, slot):
    pre = rng.choice([22, 23, 24])
    third = rng.choice([0, 4, 8, 16, 32, 64]) if pre <= 22 else rng.randint(0, 127) * 2
    net = ipaddress.ip_network(f'192.168.{third}.0/{pre}', strict=False)
    k = rng.choice([2, 4, 8])
    add = int(math.log2(k))
    subs = list(net.subnets(prefixlen_diff=add))
    show = subs[:3] if k > 2 else subs
    return dict(stem=f'The network {net} is to be divided into {k} equal subnets. State the new prefix length and subnet mask, the number of usable hosts per subnet, and the network addresses of the first {len(show)} subnets.',
                answer=f'/{pre + add} ({subs[0].netmask}); {subs[0].num_addresses - 2} hosts each; ' + ', '.join(str(s) for s in show),
                markingKey=f'Borrow log2({k}) = {add} bits → /{pre + add}, mask {subs[0].netmask} (A1); hosts 2^{32 - pre - add} − 2 = {subs[0].num_addresses - 2} (A1); subnets ' + ', '.join(str(s) for s in show) + ' (A1-2).', marks=4)


@R.add('ch05-st5', 'C3', (2, 4), 'short')
def same_subnet(rng, slot):
    pre = rng.choice([24, 25, 26, 27, 28])
    net = ipaddress.ip_network(f'10.{rng.randint(0, 255)}.{rng.randint(0, 255)}.0/{pre}', strict=False)
    a = net.network_address + rng.randint(1, net.num_addresses - 2)
    if rng.random() < 0.5:
        b = net.network_address + rng.randint(1, net.num_addresses - 2)
    else:
        b = net.broadcast_address + rng.randint(2, 40)
    same = b in net and b != net.broadcast_address
    nb = ipaddress.ip_interface(f'{b}/{pre}').network
    return dict(stem=f'Hosts X ({a}) and Y ({b}) both use the mask /{pre} ({net.netmask}). Determine whether they are on the same subnet and state whether a router is needed for them to communicate.',
                answer=('Same subnet ' + str(net) + ' – no router needed') if same else f'Different subnets ({net} and {nb}) – a router is needed',
                markingKey=f'X is in {net}; Y is in {nb} (1 mark each, by ANDing with the mask); conclusion (1 mark).', marks=3)


K.ar('ch05-st5', [
    ('A /30 subnet is often used for a point-to-point link between two routers.', 'A /30 subnet has exactly two usable host addresses.', 0, 'Both true; R explains A.'),
    ('Segmenting a network reduces broadcast traffic.', 'Broadcasts are not forwarded by routers between subnets.', 0, 'Both true; R explains A.'),
    ('A subnet mask of 255.255.255.0 means /16.', 'Each 255 in a mask represents eight network bits.', 3, 'A false (it is /24); R true.'),
])


# =============================================================================================
# ch06 A2.3 Data transmission
# =============================================================================================
R.facts('ch06-st1', F(
    terms=[('protocol', 'an agreed set of rules governing the format, timing and error handling of data exchanged between devices'),
           ('TCP/IP model', 'a four-layer model (application, transport, internet, network access/link) describing how data is sent across the internet'),
           ('TCP', 'a connection-oriented transport protocol that provides reliable, ordered delivery using sequence numbers, acknowledgements and retransmission'),
           ('UDP', 'a connectionless transport protocol that sends datagrams without acknowledgements, giving low overhead but no guarantee of delivery or order'),
           ('encapsulation', 'the process in which each layer adds its own header (and sometimes trailer) to the data passed down from the layer above'),
           ('port number', 'a 16-bit number that identifies a specific application or service on a host, e.g. 443 for HTTPS'),
           ('DNS', 'the Domain Name System, which translates domain names such as ibo.org into IP addresses')],
    facts=[('At which TCP/IP layer does IP operate?', 'Internet layer', ['Transport layer', 'Application layer', 'Link layer'], 'IP handles addressing and routing between networks.'),
           ('Which protocol is most suitable for live video calls?', 'UDP', ['TCP', 'FTP', 'SMTP'], 'Low latency matters more than retransmitting lost packets.'),
           ('Which port does HTTPS normally use?', '443', ['80', '21', '25'], 'HTTP uses 80; HTTPS uses 443.'),
           ('Which protocol is used to send email from a client to a mail server?', 'SMTP', ['IMAP', 'HTTP', 'DHCP'], 'SMTP sends; IMAP/POP3 retrieve.'),
           ('Which protocol automatically assigns IP addresses to devices joining a network?', 'DHCP', ['DNS', 'ARP', 'FTP'], 'Dynamic Host Configuration Protocol.')],
    why=[('Explain why network communication is divided into layers.', 'Each layer has a defined job and interface, so layers can be designed, changed and debugged independently (e.g. Wi-Fi replaced by Ethernet without changing HTTP), and different vendors\' products interoperate by following the same protocols.'),
         ('Explain why TCP is used for web pages and file downloads.', 'Every byte must arrive correctly and in order; TCP uses sequence numbers, acknowledgements and retransmission to guarantee this, which matters more than the small extra delay.'),
         ('Explain why DNS is needed.', 'Humans remember names more easily than IP addresses, and a service\'s IP address may change; DNS maps names to current addresses so users and programs can always find the server.')],
    contrast=[('TCP', 'UDP', 'TCP is connection-oriented and reliable (handshake, acknowledgements, retransmission, ordering) but has more overhead; UDP is connectionless with no guarantees, so it is faster and lighter, suiting streaming and gaming.'),
              ('an IP address', 'a port number', 'An IP address identifies a host on the network; a port number identifies a particular application or service on that host.')],
    misc=[('UDP is useless because it loses data.', 'UDP is preferred where speed matters and the application can tolerate or handle loss, such as VoIP, live video, DNS queries and online games.'),
          ('HTTP is responsible for routing packets across the internet.', 'HTTP is an application-layer protocol; routing is done by IP at the internet layer.'),
          ('Each layer of the TCP/IP model removes the headers of the layer above when sending.', 'When sending, each layer adds its own header (encapsulation); headers are removed on receipt (de-encapsulation).')],
    evaluate=[('TCP should be used for all internet applications because it is reliable.', ['guaranteed, ordered delivery', 'built-in congestion control'], ['handshake and retransmission add latency', 'head-of-line blocking hurts real-time media', 'newer protocols (QUIC over UDP) achieve reliability with lower latency'], 'Reliability is not always the priority; real-time applications benefit from UDP-based protocols.')],
    extended=[('A user in Singapore types https://www.example.org into a browser. Describe the protocols used at each layer of the TCP/IP model, from resolving the name to the page being displayed.', 'Application: DNS query (UDP 53) resolves the name; HTTPS (HTTP over TLS) request on port 443. Transport: TCP three-way handshake, segments with sequence numbers and acknowledgements. Internet: IP packets with source and destination IP addresses routed hop by hop. Link: Ethernet/Wi-Fi frames with MAC addresses (ARP to find the gateway). Server responds; the browser renders HTML.', 6)],
))

_PROTO = [('HTTP', 'application', 'transferring web pages'), ('HTTPS', 'application', 'secure web pages using TLS'), ('FTP', 'application', 'transferring files'),
          ('SMTP', 'application', 'sending email'), ('IMAP', 'application', 'retrieving email while keeping it on the server'), ('DNS', 'application', 'resolving domain names to IP addresses'),
          ('DHCP', 'application', 'assigning IP addresses automatically'), ('TCP', 'transport', 'reliable, ordered delivery'), ('UDP', 'transport', 'fast, connectionless delivery'),
          ('IP', 'internet', 'addressing and routing packets'), ('ICMP', 'internet', 'error and diagnostic messages (ping)'), ('Ethernet', 'link (network access)', 'sending frames on a wired LAN'),
          ('Wi-Fi (802.11)', 'link (network access)', 'sending frames over wireless LAN'), ('ARP', 'link (network access)', 'finding the MAC address for an IP address')]


@R.add('ch06-st1', 'C3', (1, 4), 'short')
def proto_layer(rng, slot):
    ps = rng.sample(_PROTO, 3 if slot.d <= 2 else 4)
    ans = '; '.join(f'{p} – {l} layer, {f}' for p, l, f in ps)
    return dict(stem=f'For each protocol, state the TCP/IP layer at which it operates and its purpose: {", ".join(p for p, _, _ in ps)}.', answer=ans,
                markingKey=f'1 mark per protocol (layer and purpose): {ans}.', marks=len(ps))


@R.add('ch06-st1', 'C3', (2, 5), 'numerical')
def encap(rng, slot):
    data = rng.choice([100, 300, 536, 1000, 1460])
    tcp = rng.choice([20, 32])
    ip = 20
    eth = 18
    proto = rng.choice(['TCP', 'UDP'])
    th = tcp if proto == 'TCP' else 8
    total = data + th + ip + eth
    eff = data / total
    return dict(stem=f'An application sends {data} bytes of data using {proto}. The transport header is {th} bytes, the IP header {ip} bytes and the Ethernet header plus trailer {eth} bytes. Describe the encapsulation and calculate the frame size and the percentage of the frame that is application data.',
                answer=f'{total} bytes; {r2(100 * eff, 1)}% data', markingKey=f'Data → {proto} segment/datagram (+{th}) → IP packet (+{ip}) → Ethernet frame (+{eth}) (1-2 marks); total = {data} + {th} + {ip} + {eth} = {total} (A1); {data}/{total} = {r2(100 * eff, 1)}% (A1).', marks=4)


K.ar('ch06-st1', [
    ('Video calls often use UDP.', 'UDP does not wait for lost packets to be retransmitted.', 0, 'Both true; avoiding retransmission delay is why.'),
    ('TCP guarantees that segments arrive in order.', 'TCP uses sequence numbers and acknowledgements.', 0, 'Both true; R explains A.'),
    ('DNS operates at the internet layer.', 'DNS translates domain names into IP addresses.', 3, 'A false (DNS is an application-layer protocol); R true.'),
])


R.facts('ch06-st2', F(
    terms=[('packet switching', 'a method of sending data in which a message is split into packets that are routed independently across the network and reassembled at the destination'),
           ('circuit switching', 'a method in which a dedicated path is set up between sender and receiver for the whole communication'),
           ('packet', 'a unit of data with a header (source and destination addresses, sequence number) and a payload'),
           ('parity bit', 'an extra bit added to a group of bits so that the total number of 1s is even (even parity) or odd (odd parity)'),
           ('checksum', 'a value calculated from a block of data and sent with it so that the receiver can recalculate it and detect errors'),
           ('cyclic redundancy check (CRC)', 'an error-detection method that treats the data as a polynomial, divides by a generator and sends the remainder'),
           ('automatic repeat request (ARQ)', 'an error-control method in which the receiver acknowledges correct data and the sender retransmits data that is not acknowledged within a timeout')],
    facts=[('Using even parity, what parity bit is added to 1011001?', '0', ['1', '2', 'It depends on the receiver'], 'There are four 1s, already even.'),
           ('Why can packets of the same message arrive out of order?', 'They may take different routes through the network', ['They are encrypted differently', 'Routers deliberately shuffle them', 'Each packet has a different destination'], 'Packets are routed independently.'),
           ('What error can a single parity bit NOT detect?', 'Two bits flipped in the same byte', ['One bit flipped', 'The parity bit itself flipped', 'Any odd number of flipped bits'], 'An even number of errors keeps the parity correct.'),
           ('What is a hop limit (TTL) in a packet header used for?', 'To stop packets circulating forever by discarding them after a number of hops', ['To encrypt the packet', 'To give the packet priority', 'To count the bytes in the payload'], 'Each router decrements TTL and drops packets at 0.')],
    why=[('Explain why packet switching uses network capacity more efficiently than circuit switching.', 'Links are shared by packets from many users and are only used when data is actually sent; in circuit switching a dedicated path is reserved for the whole call even when idle.'),
         ('Explain why a sequence number is included in each packet header.', 'Packets may take different routes and arrive out of order or be lost; sequence numbers let the receiver reassemble the data in the right order and identify missing packets to request again.'),
         ('Explain why checksums detect more errors than a single parity bit.', 'A checksum is computed over a whole block of data, so most multi-bit errors change the result, whereas a parity bit only detects an odd number of flipped bits in its group.')],
    contrast=[('packet switching', 'circuit switching', 'Packet switching splits data into independently routed packets sharing links (efficient, resilient, variable delay); circuit switching reserves a dedicated path for the whole session (constant delay, but wasteful when idle).'),
              ('error detection', 'error correction', 'Error detection only discovers that data has been corrupted (parity, checksum), usually leading to retransmission; error correction (e.g. Hamming codes) contains enough redundancy to fix errors without retransmission.')],
    misc=[('All the packets of one message must follow the same route.', 'In packet switching each packet is routed independently and may take a different route.'),
          ('A parity check can tell the receiver which bit is wrong.', 'A single parity bit only shows that an odd number of bits changed, not which one; schemes like Hamming codes or 2D parity can locate errors.'),
          ('If a checksum matches, the data is guaranteed to be correct.', 'Different data can produce the same checksum, so some errors go undetected (though rarely with strong methods like CRC).')],
    evaluate=[('Packet switching is superior to circuit switching for all communication.', ['efficient sharing of links', 'resilient – packets reroute around failures'], ['variable delay (jitter) and possible loss affect real-time voice', 'needs reassembly and more overhead per packet'], 'Packet switching dominates today and QoS mitigates jitter, but circuit switching gives guaranteed quality for some real-time uses.')],
    extended=[('A 2.4 MB image is sent across the internet in packets with a 1200-byte payload. Describe how the image is split, routed, checked for errors and reassembled, calculating the number of packets.', '2 400 000 / 1200 = 2000 packets. Each packet gets a header with source/destination IP, sequence number, TTL and checksum; routers forward each independently using routing tables; the receiver checks checksums, discards corrupted packets and requests retransmission (TCP ARQ via missing acknowledgements); packets are reordered by sequence number and reassembled into the file.', 6)],
))


@R.add('ch06-st2', 'C3', (1, 4), 'short')
def parity(rng, slot):
    bits = [rng.randint(0, 1) for _ in range(7)]
    kind = rng.choice(['even', 'odd'])
    ones = sum(bits)
    p = ones % 2 if kind == 'even' else 1 - ones % 2
    word = ''.join(map(str, bits))
    if slot.d <= 2:
        return dict(stem=f'State the parity bit that must be added to the 7-bit data {word} using {kind} parity.', answer=str(p),
                    markingKey=f'Number of 1s = {ones}; {kind} parity → parity bit {p}.', marks=1)
    recv = [p] + bits
    flips = rng.choice([0, 1, 2])
    idx = rng.sample(range(8), flips)
    for i in idx:
        recv[i] ^= 1
    rw = ''.join(map(str, recv))
    ok = (sum(recv) % 2 == 0) == (kind == 'even')
    return dict(stem=f'A system uses {kind} parity with the parity bit as the leftmost bit. The byte {rw} is received. State whether the parity check detects an error, and explain whether the byte is definitely correct.',
                answer=('Parity check passes' if ok else 'Error detected') + (' – but not definitely correct: an even number of flipped bits would not be detected' if ok else ' – the number of 1s is wrong for ' + kind + ' parity'),
                markingKey=f'Count of 1s = {sum(recv)} → {"consistent" if ok else "inconsistent"} with {kind} parity (1); conclusion (1); {"note that 2-bit errors pass undetected" if ok else "byte must be retransmitted"} (1).', marks=3)


@R.add('ch06-st2', 'C3', (2, 5), 'numerical')
def checksum(rng, slot):
    n = 4 + slot.d // 2
    data = [rng.randint(10, 255) for _ in range(n)]
    s = sum(data) % 256
    mode = rng.choice(['calc', 'check'])
    if mode == 'calc':
        return dict(stem=f'A simple checksum is the sum of the data bytes modulo 256. Calculate the checksum for the bytes {", ".join(map(str, data))}.', answer=str(s),
                    markingKey=f'Sum = {sum(data)} (M1); {sum(data)} mod 256 = {s} (A1).', marks=2)
    bad = data[:]
    i = rng.randrange(n)
    bad[i] = (bad[i] + rng.randint(1, 50)) % 256
    corrupted = rng.random() < 0.6
    recv = bad if corrupted else data
    rs = sum(recv) % 256
    return dict(stem=f'Data is sent with a checksum equal to the sum of the bytes modulo 256. The receiver gets the bytes {", ".join(map(str, recv))} with the checksum {s}. Determine whether an error has been detected and state what happens next.',
                answer=('Error detected' if rs != s else 'No error detected') + f' (recalculated checksum {rs})' + ('; the receiver requests retransmission (no ACK sent)' if rs != s else '; the receiver sends an acknowledgement'),
                markingKey=f'Recalculated sum {sum(recv)} mod 256 = {rs} (M1 A1); compare with {s} (R1); action (1).', marks=4)


@R.add('ch06-st2', 'C3', (2, 4), 'numerical')
def packets_count(rng, slot):
    size = rng.choice([0.5, 1.2, 2.4, 3.6, 10]) * 1e6
    pay = rng.choice([500, 1000, 1200, 1460])
    hdr = rng.choice([20, 40])
    n = math.ceil(size / pay)
    total = size + n * hdr
    return dict(stem=f'A {r2(size / 1e6)} MB file (1 MB = 10^6 bytes) is sent using packets that each carry up to {pay} bytes of data plus a {hdr}-byte header. Calculate the number of packets and the total number of bytes transmitted.',
                answer=f'{n:,} packets; {total:,.0f} bytes', markingKey=f'⌈{size:,.0f}/{pay}⌉ = {n:,} (M1 A1); total = {size:,.0f} + {n:,}×{hdr} = {total:,.0f} (A1).', marks=3)


K.ar('ch06-st2', [
    ('Packets from the same file can arrive out of order.', 'Each packet is routed independently.', 0, 'Both true; R explains A.'),
    ('A single parity bit detects all two-bit errors.', 'Flipping two bits leaves the number of 1s with the same parity.', 3, 'A false; R true – and is why A is false.'),
    ('Circuit switching wastes capacity during silences in a call.', 'The dedicated path is reserved for the whole call.', 0, 'Both true; R explains A.'),
])


R.facts('ch06-st3', F(
    terms=[('IP address', 'a logical numeric address assigned to a network interface that identifies it on an IP network'),
           ('IPv4', 'the version of IP that uses 32-bit addresses written as four denary octets, e.g. 192.0.2.10, giving about 4.3 billion addresses'),
           ('IPv6', 'the version of IP that uses 128-bit addresses written as eight groups of four hexadecimal digits, giving about 3.4 × 10^38 addresses'),
           ('private IP address', 'an address from a reserved range (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) used inside local networks and not routed on the internet'),
           ('NAT (network address translation)', 'a technique in which a router replaces private addresses with its own public address so many devices can share one public IP'),
           ('static IP address', 'an IP address that is manually configured and does not change'),
           ('dynamic IP address', 'an IP address assigned automatically for a limited time, normally by a DHCP server')],
    facts=[('How many bits are in an IPv6 address?', '128', ['32', '64', '48'], 'IPv6 uses 128-bit addresses.'),
           ('Which of these is a private IPv4 address?', '192.168.4.20', ['8.8.8.8', '203.0.113.5', '151.101.1.69'], '192.168.0.0/16 is reserved for private use.'),
           ('What was the main reason for introducing IPv6?', 'IPv4 addresses were running out', ['IPv4 was too slow', 'IPv4 could not carry video', 'IPv6 addresses are shorter'], '4.3 billion addresses are not enough for every device.'),
           ('Which address is the IPv4 loopback address?', '127.0.0.1', ['0.0.0.0', '255.255.255.255', '192.168.0.1'], 'Packets to 127.0.0.1 never leave the host.')],
    why=[('Explain why NAT has delayed the exhaustion of IPv4 addresses.', 'Many devices in a home or organisation use private addresses and share one public IPv4 address through the router\'s NAT, so far fewer public addresses are needed.'),
         ('Explain why a web server is usually given a static IP address.', 'Clients and DNS records must find the server at a predictable address; if it changed (dynamic), DNS would need updating and connections would fail.'),
         ('Explain why IPv6 addresses are written in hexadecimal.', '128 bits written in denary would be very long; hex groups of 16 bits (4 hex digits) are compact, and leading zeros and runs of zero groups can be abbreviated.')],
    contrast=[('IPv4', 'IPv6', 'IPv4 uses 32-bit addresses (~4.3 billion) in dotted denary; IPv6 uses 128-bit addresses (~3.4 × 10^38) in colon-separated hex, with simpler headers and no need for NAT.'),
              ('a static IP address', 'a dynamic IP address', 'A static address is set manually and stays the same (servers, printers); a dynamic address is leased automatically by DHCP and may change (laptops, phones).'),
              ('a public IP address', 'a private IP address', 'A public address is globally unique and routable on the internet; a private address is from a reserved range used only within local networks and must be translated (NAT) to reach the internet.')],
    misc=[('IPv6 addresses are four times as many as IPv4 addresses because they are four times longer.', 'Each extra bit doubles the number of addresses: 2^128 is 2^96 times more than 2^32, not four times.'),
          ('Two homes cannot both use 192.168.1.10 because IP addresses must be unique.', 'Private addresses only need to be unique within a local network; NAT gives each home one unique public address.'),
          ('A device\'s IP address never changes.', 'Dynamic addresses assigned by DHCP can change each time the device joins a network; MAC addresses are the (normally) fixed hardware addresses.')],
    evaluate=[('The world should switch off IPv4 and use only IPv6.', ['vastly more addresses, end-to-end connectivity', 'simpler headers and built-in autoconfiguration'], ['legacy devices and software only support IPv4', 'transition requires investment and staff training', 'NAT has extended IPv4\'s life'], 'IPv6 is the long-term future, but dual-stack operation will be needed for years.')],
    extended=[('A city council in Nairobi is deploying 50 000 smart streetlights, each needing its own address. Discuss whether it should use IPv4 with NAT or IPv6, considering address supply, management, security and compatibility.', 'IPv4 + NAT: works with existing equipment, private ranges (10.0.0.0/8) suffice internally, but NAT complicates direct reachability and monitoring and public addresses are scarce. IPv6: abundant globally unique addresses, autoconfiguration (SLAAC), end-to-end reachability (needs strong firewalling), but some devices/ISPs may lack support. IPv6 (possibly dual-stack) is the better long-term choice.', 6)],
))


@R.add('ch06-st3', 'C3', (1, 4), 'short')
def ip_classify(rng, slot):
    pool = ['10.4.22.7', '172.20.1.5', '172.32.1.5', '192.168.0.254', '8.8.4.4', '127.0.0.1', '203.0.113.9', '169.254.10.3', '100.64.0.1', '172.15.200.1', '1.1.1.1', '192.169.1.1']
    xs = rng.sample(pool, 3 if slot.d <= 2 else 4)
    def kind(a):
        ip = ipaddress.ip_address(a)
        if ip.is_loopback:
            return 'loopback'
        if ip.is_link_local:
            return 'link-local (APIPA, no DHCP server reached)'
        if ip in ipaddress.ip_network('100.64.0.0/10'):
            return 'shared address space (carrier-grade NAT), not public'
        if any(ip in ipaddress.ip_network(n) for n in ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16')):
            return 'private'
        if ip in ipaddress.ip_network('203.0.113.0/24'):
            return 'reserved documentation range (TEST-NET-3), not routable'
        return 'public'
    ans = '; '.join(f'{a} – {kind(a)}' for a in xs)
    return dict(stem=f'Classify each IPv4 address as public, private or special-purpose: {", ".join(xs)}.', answer=ans,
                markingKey=f'1 mark each: {ans}. Private ranges: 10.0.0.0/8, 172.16.0.0/12 (172.16-172.31), 192.168.0.0/16.', marks=len(xs))


@R.add('ch06-st3', 'C3', (2, 5), 'short')
def ipv6_short(rng, slot):
    groups = [0] * 8
    groups[0] = 0x2001
    groups[1] = rng.choice([0x0db8, 0x0470, 0x4860])
    for i in range(2, 8):
        groups[i] = rng.choice([0, 0, 0, 0, rng.randint(1, 0xffff), rng.randint(1, 0xff)])
    full = ':'.join(f'{g:04x}' for g in groups)
    short = ipaddress.IPv6Address(full).compressed
    if full == short:
        return None
    if rng.random() < 0.5 or slot.d <= 3:
        return dict(stem=f'Write the IPv6 address {full} in its shortest form.', answer=short,
                    markingKey=f'{short}: remove leading zeros in each group (1) and replace the longest run of two or more all-zero groups with :: (only once; a single zero group is written as 0) (1).', marks=2)
    return dict(stem=f'Expand the abbreviated IPv6 address {short} to its full form with eight groups of four hexadecimal digits.', answer=full,
                markingKey=f'{full}: restore leading zeros (1) and the zero groups represented by :: (1).', marks=2)


@R.add('ch06-st3', 'C3', (2, 4), 'numerical')
def addr_count(rng, slot):
    a, b = rng.choice([(32, 128), (32, 64), (24, 32), (16, 32), (48, 64)])
    ratio = 2 ** (b - a)
    return dict(stem=f'Compare the number of addresses provided by a {a}-bit address space and a {b}-bit address space, giving the ratio as a power of 2 and in standard form.',
                answer=f'2^{a} ≈ {2 ** a:.3e} vs 2^{b} ≈ {2 ** b:.3e}; ratio 2^{b - a} ≈ {ratio:.3e}', markingKey=f'2^{a} and 2^{b} (1 each); ratio 2^{b} / 2^{a} = 2^{b - a} ≈ {ratio:.3e} (1).', marks=3)


K.ar('ch06-st3', [
    ('Private IP addresses cannot be routed on the public internet.', 'Many separate networks reuse the same private ranges.', 0, 'Both true; because they are reused they cannot be globally unique, so they are not routed.'),
    ('IPv6 removes the need for NAT.', 'IPv6 provides enough addresses for every device to have a globally unique address.', 0, 'Both true; R explains A.'),
    ('A laptop always keeps the same IP address.', 'DHCP leases addresses to devices for a limited time.', 3, 'A false; R true and explains why.'),
])


R.facts('ch06-st4', F(
    terms=[('routing', 'the process of choosing paths across interconnected networks along which packets are forwarded'),
           ('routing table', 'a table held by a router listing destination networks, the next hop or interface to use, and a metric'),
           ('static routing', 'routing in which routes are entered manually by an administrator and do not change unless edited'),
           ('dynamic routing', 'routing in which routers exchange information using a routing protocol and update their tables automatically when the network changes'),
           ('metric', 'a value such as hop count, delay or bandwidth cost used to compare routes'),
           ('default route', 'the route used for any destination not listed in the routing table, often written 0.0.0.0/0'),
           ('link-state routing', 'a dynamic routing approach (e.g. OSPF) in which each router learns the full topology and computes shortest paths using Dijkstra\'s algorithm')],
    facts=[('Which routing approach adapts automatically when a link fails?', 'Dynamic routing', ['Static routing', 'Default routing only', 'Source routing by the user'], 'Routers exchange updates and recompute paths.'),
           ('Which algorithm is used by link-state protocols such as OSPF to find the shortest paths?', 'Dijkstra\'s algorithm', ['Bubble sort', 'Binary search', 'Round robin'], 'Dijkstra computes least-cost paths from a source.'),
           ('A small office with one connection to its ISP is most likely to use…', 'a static default route', ['a full dynamic routing protocol', 'circuit switching', 'no routing at all'], 'With one exit, a single static default route is simplest.'),
           ('In RIP, what metric is used to choose routes?', 'Hop count', ['Bandwidth only', 'Packet size', 'Cable colour'], 'RIP picks the route with the fewest hops (max 15).')],
    why=[('Explain why dynamic routing is used in large networks such as the internet.', 'There are too many routes to configure by hand and links change constantly; routing protocols exchange information automatically, find new paths around failures and balance load without administrator intervention.'),
         ('Explain why static routing can be more secure than dynamic routing.', 'Routes cannot be changed by forged routing updates from other routers, and no routing protocol traffic reveals the network\'s structure; only the administrator can alter routes.'),
         ('Explain why the lowest-hop route is not always the fastest route.', 'Hop count ignores the bandwidth, delay and congestion of each link; a route with more hops over fast, uncongested links can deliver packets sooner.')],
    contrast=[('static routing', 'dynamic routing', 'Static routes are configured manually – simple, predictable, no overhead, but do not adapt to failures; dynamic routing uses protocols to update routes automatically – adaptive and scalable but uses bandwidth/CPU and is more complex.'),
              ('distance-vector routing', 'link-state routing', 'Distance-vector routers share their tables with neighbours and know only distances/next hops (e.g. RIP); link-state routers flood link information so each knows the full topology and runs Dijkstra (e.g. OSPF), converging faster.')],
    misc=[('Each router knows the complete path a packet will take to its destination.', 'Routers forward hop by hop, normally knowing only the next hop for each destination network.'),
          ('Static routing is always worse than dynamic routing.', 'Static routes are ideal for small or stub networks and for security-sensitive links where predictability matters.'),
          ('If a link fails, static routes are updated automatically.', 'Static routes stay until an administrator changes them, so traffic may be lost.')],
    evaluate=[('Dynamic routing should be used in every network.', ['automatic adaptation to failures', 'scales to large networks'], ['overhead and complexity', 'security risk of spoofed updates', 'unnecessary for single-exit networks'], 'Essential for large or redundant networks; static routing is better for small, simple or security-critical paths.')],
    extended=[('An ISP in Santiago has six routers with links of different costs. Explain how a link-state protocol builds routing tables, apply Dijkstra\'s algorithm conceptually, and discuss what happens when a link fails.', 'Each router discovers neighbours and link costs, floods link-state advertisements so all routers share the same topology map, then runs Dijkstra from itself: start with cost 0, repeatedly choose the unvisited router with the smallest tentative cost and update its neighbours, producing a shortest-path tree; the first hop on each path goes into the routing table. On failure, adjacent routers flood updates and every router recomputes, converging on new routes.', 6)],
))


def _dijkstra(adj, src):
    dist = {n: math.inf for n in adj}
    prev = {}
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v] or (d + w == dist[v] and u < prev.get(v, 'ZZ')):
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def _graph(rng, n):
    nodes = list('ABCDEFG')[:n]
    edges = {}
    for i in range(1, n):
        edges[frozenset((nodes[i], rng.choice(nodes[:i])))] = rng.randint(1, 9)
    for _ in range(n):
        a, b = rng.sample(nodes, 2)
        edges.setdefault(frozenset((a, b)), rng.randint(1, 9))
    adj = {x: [] for x in nodes}
    for e, w in edges.items():
        a, b = sorted(e)
        adj[a].append((b, w)); adj[b].append((a, w))
    return nodes, edges, adj


def _path(prev, src, dst):
    p = [dst]
    while p[-1] != src:
        p.append(prev[p[-1]])
    return p[::-1]


@R.add('ch06-st4', 'C3', (2, 5), 'short')
def dijkstra_q(rng, slot):
    n = 5 if slot.d <= 3 else 6
    for _ in range(20):
        nodes, edges, adj = _graph(rng, n)
        dist, prev = _dijkstra(adj, 'A')
        dst = nodes[-1]
        # require a unique shortest path to dst
        cnt = {x: 0 for x in nodes}
        cnt['A'] = 1
        for x in sorted(nodes, key=lambda z: dist[z]):
            for v, w in adj[x]:
                if dist[x] + w == dist[v]:
                    cnt[v] += cnt[x]
        if cnt[dst] == 1 and len(_path(prev, 'A', dst)) >= 3:
            break
    else:
        return None
    links = ', '.join(f'{"-".join(sorted(e))} ({w})' for e, w in sorted(edges.items(), key=lambda kv: sorted(kv[0])))
    path = _path(prev, 'A', dst)
    stem = f'Routers are connected by links with these costs: {links}. Use Dijkstra\'s algorithm to find the least-cost path from router A to router {dst} and its total cost.'
    ans = f'{"→".join(path)}, cost {dist[dst]}'
    key = 'Final distances from A: ' + ', '.join(f'{x} {dist[x]}' for x in nodes) + f'. Path {ans}. 1 mark for correct working (tentative distances updated in order of smallest cost), 1 for the path, 1 for the cost.'
    if slot.d >= 4:
        nh = {x: _path(prev, 'A', x)[1] for x in nodes if x != 'A'}
        stem += ' Also give A\'s routing table (destination → next hop).'
        ans += '; next hops: ' + ', '.join(f'{k}→{v}' for k, v in nh.items())
        key += ' Routing table: ' + ', '.join(f'{k} via {v}' for k, v in nh.items()) + ' (1-2 marks).'
    return dict(stem=stem, answer=ans, markingKey=key, marks=5 if slot.d >= 4 else 3)


@R.add('ch06-st4', 'C3', (2, 4), 'short')
def route_lookup(rng, slot):
    routes = [('10.1.0.0/16', 'R2'), ('10.1.5.0/24', 'R3'), ('192.168.0.0/16', 'R4'), ('0.0.0.0/0', 'ISP')]
    dests = ['10.1.5.77', '10.1.9.3', '192.168.20.4', '8.8.8.8', '10.2.0.1', '10.1.5.200']
    ds = rng.sample(dests, 3)
    def look(d):
        best = max((r for r in routes if ipaddress.ip_address(d) in ipaddress.ip_network(r[0])), key=lambda r: ipaddress.ip_network(r[0]).prefixlen)
        return best
    ans = '; '.join(f'{d} → {look(d)[1]} (matches {look(d)[0]})' for d in ds)
    return dict(stem='A router\'s table is: ' + '; '.join(f'{n} via {h}' for n, h in routes) + f'. Routers choose the longest (most specific) matching prefix. State the next hop for packets addressed to {", ".join(ds)}.',
                answer=ans, markingKey=f'1 mark each: {ans}.', marks=3)


K.ar('ch06-st4', [
    ('Dynamic routing can reroute traffic around a failed link.', 'Routers running a routing protocol exchange updates about changes in the network.', 0, 'Both true; R explains A.'),
    ('Static routes are configured automatically by routers.', 'Static routes do not change unless an administrator edits them.', 3, 'A false; R true.'),
    ('OSPF uses Dijkstra\'s algorithm.', 'OSPF routers share link-state information so each knows the topology.', 0, 'Both true; knowing the full topology lets each router run Dijkstra.'),
])


R.facts('ch06-st5', F(
    terms=[('bandwidth', 'the maximum rate at which data can be transmitted over a connection, measured in bits per second'),
           ('latency', 'the time delay for data to travel from source to destination, usually measured in milliseconds'),
           ('throughput', 'the actual rate of successful data transfer achieved, which is usually less than the bandwidth'),
           ('fibre-optic cable', 'a transmission medium that carries data as pulses of light along glass or plastic fibres'),
           ('twisted-pair cable', 'copper cable in which pairs of wires are twisted together to reduce interference, used in Ethernet LANs'),
           ('attenuation', 'the gradual loss of signal strength as it travels through a medium'),
           ('jitter', 'variation in latency between packets, which disrupts real-time audio and video')],
    facts=[('Which transmission medium is immune to electromagnetic interference?', 'Fibre-optic cable', ['Unshielded twisted pair', 'Coaxial cable', 'Wi-Fi'], 'Light signals are unaffected by electrical noise.'),
           ('Which factor most affects the delay of a satellite internet connection?', 'The long distance the signal travels to geostationary orbit and back', ['The colour of the dish', 'The size of the file', 'The type of browser'], 'Propagation delay of ~0.25 s per round trip.'),
           ('A link has a bandwidth of 100 Mbit/s but downloads only reach 60 Mbit/s. The 60 Mbit/s is the…', 'throughput', ['bandwidth', 'latency', 'jitter'], 'Throughput is the achieved rate.'),
           ('Which medium is most suitable for connecting two buildings 2 km apart?', 'Single-mode fibre-optic cable', ['Cat 5e twisted pair', 'Bluetooth', 'Coaxial cable'], 'Copper Ethernet is limited to about 100 m.')],
    why=[('Explain why fibre-optic cable is used for long-distance backbone links.', 'Light in fibre suffers very little attenuation and no electromagnetic interference, so very high bandwidths can be carried over many kilometres without repeaters, and it is hard to tap.'),
         ('Explain why high latency matters more for online gaming than for downloading a large file.', 'Gaming exchanges many small, time-sensitive messages, so every round trip delay is noticed as lag; a large download is limited mainly by bandwidth and the initial delay is insignificant compared with the total time.'),
         ('Explain why wireless connections usually have lower throughput than wired ones.', 'The radio medium is shared by all devices, suffers interference and attenuation through walls, and needs extra overhead for collision avoidance and retransmissions.')],
    contrast=[('bandwidth', 'latency', 'Bandwidth is how much data can be sent per second (capacity); latency is how long a piece of data takes to arrive (delay). A link can have high bandwidth but high latency (satellite).'),
              ('fibre-optic cable', 'twisted-pair copper cable', 'Fibre carries light – very high bandwidth, long distances, no EM interference, but more expensive and fragile; twisted pair carries electrical signals – cheap and easy to install but limited to about 100 m and affected by interference.')],
    misc=[('A 100 Mbit/s connection downloads a 100 MB file in one second.', 'Bits and bytes differ: 100 MB = 800 Mbit, so it takes at least 8 s, plus overheads and latency.'),
          ('Higher bandwidth always reduces latency.', 'Bandwidth affects transmission time, but propagation delay depends on distance and the speed of the signal; a fast satellite link still has high latency.'),
          ('Fibre-optic cables carry data using electricity.', 'Fibre carries pulses of light, not electrical current.')],
    evaluate=[('Fibre-to-the-home should replace all copper connections in a country.', ['much higher bandwidth and future-proof', 'lower attenuation and maintenance'], ['very high installation cost, especially rural areas', '5G/fixed wireless may be cheaper for remote regions'], 'Fibre is the best long-term medium for dense areas; mixed approaches suit sparse regions.')],
    extended=[('A research team in Antarctica must send 200 GB of data per day to a university in Hobart. Compare a geostationary satellite link (50 Mbit/s, 600 ms latency), a low-earth-orbit satellite link (150 Mbit/s, 40 ms) and physically shipping drives, using calculations.', 'GEO: 200 GB = 1.6 × 10^12 bits / 50 × 10^6 = 32 000 s ≈ 8.9 h per day; LEO: 1.6 × 10^12 / 150 × 10^6 ≈ 10 667 s ≈ 3 h; shipping: huge bandwidth but days of latency. LEO is best for daily transfer and interactive work; GEO workable but slow; shipping only for archives. Consider cost, weather and reliability.', 6)],
))


@R.add('ch06-st5', 'C3', (1, 5), 'numerical')
def tx_time(rng, slot):
    size = rng.choice([5, 25, 120, 700, 4000])
    unit = rng.choice(['MB', 'GB']) if size < 700 else 'MB'
    bw = rng.choice([8, 20, 50, 100, 300, 1000])
    bits = size * (1e6 if unit == 'MB' else 1e9) * 8
    t = bits / (bw * 1e6)
    stem = f'Calculate the time to transfer a {size} {unit} file (1 {unit} = 10^{6 if unit == "MB" else 9} bytes) over a {bw} Mbit/s connection'
    key = f'{size} {unit} × 8 = {bits:,.0f} bits (M1); ÷ {bw}×10^6 = {r2(t, 2)} s (A1).'
    ans = f'{r2(t, 2)} s'
    m = 2
    if slot.d >= 3:
        eff = rng.choice([70, 80, 90])
        lat = rng.choice([20, 40, 120, 600])
        t2 = t / (eff / 100) + lat / 1000
        stem += f', and the total time if throughput is only {eff}% of the bandwidth and there is a one-off latency of {lat} ms'
        ans += f'; {r2(t2, 2)} s with throughput and latency'
        key += f' Actual = {r2(t, 2)}/{eff / 100} + {lat / 1000} = {r2(t2, 2)} s (M1 A1).'
        m = 4
    return dict(stem=stem + '.', answer=ans, markingKey=key, marks=m)


@R.add('ch06-st5', 'C3', (2, 5), 'numerical')
def prop_delay(rng, slot):
    medium, v = rng.choice([('fibre-optic cable', 2e8), ('copper cable', 2e8), ('radio link to a geostationary satellite (in vacuum)', 3e8)])
    dist = rng.choice([500, 2000, 6000, 12000]) * 1000 if 'satellite' not in medium else 35786e3 * 2
    t = dist / v
    return dict(stem=f'A signal travels {dist / 1000:,.0f} km through {medium} at about {v:.0e} m/s. Calculate the propagation delay in milliseconds and explain its effect on interactive applications.',
                answer=f'{r2(t * 1000, 1)} ms', markingKey=f'{dist:,.0f} m ÷ {v:.0e} m/s = {r2(t, 4)} s = {r2(t * 1000, 1)} ms (M1 A1); a round trip doubles this, adding noticeable lag for gaming/video calls (R1).', marks=3)


@R.add('ch06-st5', 'C3', (1, 4), 'short')
def media_choice(rng, slot):
    items = [('linking two campus buildings 1.5 km apart', 'single-mode fibre', 'long distance with low attenuation and high bandwidth'),
             ('connecting desktop PCs to a switch in the same room', 'Cat 6 twisted pair', 'cheap, easy to install, supports 1-10 Gbit/s up to 100 m'),
             ('a factory floor with heavy electrical machinery', 'fibre-optic (or shielded twisted pair)', 'immune/resistant to electromagnetic interference'),
             ('visitors\' phones in a museum', 'Wi-Fi (radio)', 'mobility without cables for many temporary devices'),
             ('a research station in a remote desert', 'satellite link', 'no cable infrastructure is available'),
             ('a temporary outdoor concert stage', 'wireless point-to-point link or ruggedised cable', 'quick to set up and remove')]
    who, m, why = rng.choice(items)
    return dict(stem=f'Recommend a transmission medium for {who} and justify it with reference to bandwidth, distance or interference.', answer=f'{m}: {why}.',
                markingKey=f'{m} (1); justification: {why} (1-2).', marks=3)


K.ar('ch06-st5', [
    ('Satellite internet often has high latency.', 'Signals must travel tens of thousands of kilometres to and from the satellite.', 0, 'Both true; R explains A.'),
    ('Throughput is usually lower than bandwidth.', 'Protocol overheads, congestion and retransmissions reduce the achieved rate.', 0, 'Both true; R explains A.'),
    ('Fibre-optic cables are affected by electromagnetic interference.', 'Fibre carries data as pulses of light.', 3, 'A false; R true and is why A is false.'),
])


# =============================================================================================
# ch07 A2.4 Network security
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('malware', 'malicious software, such as viruses, worms, trojans, ransomware and spyware, designed to damage systems or steal data'),
           ('phishing', 'sending fraudulent messages that appear to come from a trusted source to trick people into revealing information or installing malware'),
           ('denial-of-service (DoS) attack', 'an attack that floods a server or network with traffic so legitimate users cannot access it; distributed (DDoS) when many machines are used'),
           ('man-in-the-middle (MitM) attack', 'an attack in which the attacker secretly intercepts, and possibly alters, communication between two parties'),
           ('SQL injection', 'an attack in which malicious SQL is entered into an input field so that it is executed by the database'),
           ('social engineering', 'manipulating people into breaking security procedures, for example by impersonating IT staff'),
           ('ransomware', 'malware that encrypts the victim\'s files and demands payment for the decryption key'),
           ('brute-force attack', 'trying every possible password or key until the correct one is found')],
    facts=[('Which type of malware spreads across a network by itself without attaching to a file?', 'Worm', ['Virus', 'Trojan', 'Spyware'], 'Worms self-replicate across networks.'),
           ('An email that appears to be from a bank asks the user to "confirm" their password on a link. This is…', 'phishing', ['a DDoS attack', 'SQL injection', 'a brute-force attack'], 'It tricks the user into revealing credentials.'),
           ('Which measure best protects against SQL injection?', 'Parameterised queries (prepared statements)', ['A stronger Wi-Fi password', 'Defragmenting the disk', 'Using a faster server'], 'Input is never executed as SQL code.'),
           ('Which is the best defence against ransomware destroying data?', 'Regular offline backups', ['A larger hard disk', 'Using HTTP instead of HTTPS', 'Disabling the firewall'], 'Files can be restored without paying.')],
    why=[('Explain why social engineering is often more effective than technical attacks.', 'It targets people, who can be persuaded by urgency, authority or trust to reveal passwords or open attachments, bypassing technical controls such as firewalls and encryption entirely.'),
         ('Explain why a DDoS attack is harder to stop than a DoS attack from one computer.', 'Traffic comes from thousands of compromised machines (a botnet) with different IP addresses, so blocking one address does not help, and the attack traffic can look like legitimate requests.'),
         ('Explain why long passwords resist brute-force attacks.', 'Each extra character multiplies the number of possible passwords by the size of the character set, so the search space grows exponentially and the time needed becomes impractically large.')],
    contrast=[('a virus', 'a worm', 'A virus attaches itself to a host file and needs a user action to spread; a worm is standalone and spreads automatically across networks by exploiting vulnerabilities.'),
              ('phishing', 'pharming', 'Phishing tricks users with fake messages and links; pharming redirects users from a genuine address to a fake site, e.g. by poisoning DNS, without them clicking a bad link.')],
    misc=[('Antivirus software alone makes a computer completely secure.', 'Antivirus only detects known or suspicious malware; updates, firewalls, backups, strong authentication and user awareness are also needed.'),
          ('Only large companies are targeted by cyberattacks.', 'Automated attacks scan every device and small organisations and individuals are frequent targets because they often have weaker defences.'),
          ('A trojan replicates itself across the network.', 'A trojan disguises itself as useful software and does not self-replicate; worms self-replicate.')],
    evaluate=[('User training is more important than technical security measures.', ['most breaches involve human error such as phishing', 'training is relatively cheap'], ['technical measures stop automated attacks that never involve users', 'people still make mistakes after training'], 'Both are essential; training reduces human risk while technical controls provide defence in depth.')],
    extended=[('A secondary school in Melbourne has suffered a ransomware attack that began with a phishing email to a teacher. Analyse how the attack probably happened and recommend technical and human measures to prevent a repeat.', 'Phishing email → teacher clicked link/attachment → malware installed → spread across network shares → files encrypted. Measures: email filtering and attachment sandboxing; MFA; patching; least-privilege accounts; network segmentation; endpoint protection; regular offline/immutable backups and a tested recovery plan; staff training and phishing simulations; incident response plan.', 6)],
))


@R.add('ch07-st1', 'C3', (2, 5), 'numerical')
def brute_force(rng, slot):
    sets = [('digits only', 10), ('lower-case letters', 26), ('upper- and lower-case letters', 52), ('letters and digits', 62), ('all 94 printable symbols', 94)]
    (desc, c) = rng.choice(sets)
    L = rng.choice([4, 6, 8, 10, 12])
    rate = rng.choice([1e6, 1e9, 1e10])
    n = c ** L
    t = n / rate
    def human(sec):
        for u, s in ((365.25 * 86400, 'years'), (86400, 'days'), (3600, 'hours'), (60, 'minutes')):
            if sec >= u:
                return f'{sec / u:.3g} {s}'
        return f'{sec:.3g} seconds'
    return dict(stem=f'A password is {L} characters long and uses {desc}. An attacker can test {rate:,.0f} passwords per second. Calculate the number of possible passwords and the maximum time to try them all.',
                answer=f'{c}^{L} = {n:.3e} passwords; at most {human(t)}', markingKey=f'{c}^{L} = {n:.3e} (M1 A1); ÷ {rate:.0e} per second = {t:.3e} s ≈ {human(t)} (A1). Average time is half this.', marks=3)


_THREATS = [('Staff receive an email claiming their mailbox is full, with a link to a login page that copies the address bar of the real one.', 'phishing', 'user training, email filtering, MFA'),
            ('A website\'s login form is given the input  \' OR \'1\'=\'1  and the attacker is logged in without a password.', 'SQL injection', 'parameterised queries and input validation'),
            ('An online shop becomes unreachable as 40 000 IoT devices send it requests simultaneously.', 'DDoS attack', 'DDoS mitigation service/CDN, rate limiting, traffic filtering'),
            ('On café Wi-Fi an attacker sets up a hotspot with the same name and reads unencrypted traffic.', 'man-in-the-middle (evil twin)', 'HTTPS/VPN, verifying networks, avoiding open Wi-Fi'),
            ('A free "PDF converter" download secretly installs software that records keystrokes.', 'trojan / spyware (keylogger)', 'download only from trusted sources, anti-malware, least privilege'),
            ('A caller pretending to be from IT asks a receptionist to read out a one-time login code.', 'social engineering (vishing)', 'verification procedures and staff training'),
            ('Files on a shared drive are suddenly renamed with .locked and a note demands Bitcoin.', 'ransomware', 'offline backups, patching, segmentation, endpoint protection'),
            ('Malware spreads from one unpatched PC to every other unpatched PC on the LAN without user action.', 'worm', 'patch management, firewalls and network segmentation')]


@R.add('ch07-st1', 'C3', (1, 4), 'short')
def threat_id(rng, slot):
    sc, th, fix = rng.choice(_THREATS)
    return dict(stem=f'{sc} Identify the type of threat and suggest two measures that would reduce the risk.', answer=f'{th}; measures: {fix}.',
                markingKey=f'Threat: {th} (1); two appropriate measures, e.g. {fix} (1 each).', marks=3)


K.ar('ch07-st1', [
    ('Parameterised queries prevent SQL injection.', 'User input is treated as data and not executed as SQL.', 0, 'Both true; R explains A.'),
    ('A worm needs a user to open an infected file in order to spread.', 'Worms exploit network vulnerabilities.', 3, 'A false (worms self-propagate); R true.'),
    ('Offline backups reduce the impact of ransomware.', 'Ransomware cannot encrypt files on media that is disconnected.', 0, 'Both true; R explains A.'),
])


R.facts('ch07-st2', F(
    terms=[('firewall', 'hardware or software that monitors incoming and outgoing network traffic and allows or blocks it according to a set of rules'),
           ('packet-filtering firewall', 'a firewall that inspects each packet\'s header (IP addresses, ports, protocol) and applies rules without examining the payload'),
           ('stateful inspection', 'firewall filtering that tracks the state of connections and only allows packets belonging to established, legitimate sessions'),
           ('proxy server', 'a server that acts as an intermediary between clients and other servers, forwarding requests so clients are not directly exposed'),
           ('intrusion detection system (IDS)', 'a system that monitors network or host activity for suspicious patterns and raises alerts'),
           ('intrusion prevention system (IPS)', 'a system that detects suspicious activity and automatically blocks it'),
           ('DMZ (demilitarised zone)', 'a separate network segment that hosts public-facing servers, isolated from the internal network by firewalls')],
    facts=[('A firewall rule list is processed top to bottom. What usually happens to a packet that matches no rule?', 'It is handled by the default policy, usually deny', ['It is always allowed', 'It is sent back to the sender', 'It is forwarded to the IDS for encryption'], 'Default-deny is best practice.'),
           ('Which device can cache web pages and hide internal users\' IP addresses?', 'Proxy server', ['Hub', 'Repeater', 'Modem'], 'Proxies forward requests on behalf of clients.'),
           ('What is the main difference between an IDS and an IPS?', 'An IPS can automatically block traffic; an IDS only alerts', ['An IDS encrypts traffic', 'An IPS is only for wireless networks', 'An IDS replaces the firewall'], 'Prevention vs detection.'),
           ('A company\'s public web server should be placed in…', 'a DMZ', ['the internal staff LAN', 'the backup room', 'the same VLAN as the finance database'], 'If compromised it does not give direct access to internal systems.')],
    why=[('Explain why firewall rules should follow a default-deny policy.', 'Only traffic that is explicitly needed is permitted, so new services, misconfigurations or unexpected ports are blocked automatically; a default-allow policy would let anything through that the administrator forgot to block.'),
         ('Explain why the order of firewall rules matters.', 'Rules are checked top to bottom and the first match is applied, so a broad allow rule above a specific deny rule would let the unwanted traffic through; specific rules must come before general ones.'),
         ('Explain why an IDS may produce false positives.', 'Anomaly-based detection flags unusual but legitimate behaviour (e.g. a new backup job) and signatures may match innocent traffic, so alerts must be reviewed and rules tuned.')],
    contrast=[('a firewall', 'an IDS', 'A firewall enforces rules to allow or block traffic at a boundary; an IDS monitors traffic and activity for signs of attack and alerts, without blocking by itself.'),
              ('signature-based detection', 'anomaly-based detection', 'Signature-based detection matches known attack patterns (accurate but misses new attacks); anomaly-based detection flags deviations from normal behaviour (can catch new attacks but produces more false positives).')],
    misc=[('A firewall protects against all types of attack.', 'Firewalls do not stop phishing, malware brought in on USB drives, insider threats or attacks hidden in allowed traffic such as HTTPS.'),
          ('A proxy server encrypts all traffic automatically.', 'A proxy forwards requests; encryption depends on the protocol (HTTPS, VPN).'),
          ('An IDS stops attacks as they happen.', 'An IDS detects and alerts; an IPS (or a human response) is needed to block.')],
    evaluate=[('A well-configured firewall is enough to protect a small business network.', ['blocks unsolicited inbound traffic and limits outbound ports'], ['cannot stop phishing, malware in allowed traffic or insiders', 'remote workers bypass the perimeter', 'no visibility of attacks without an IDS/logging'], 'A firewall is necessary but must be part of layered security (defence in depth).')],
    extended=[('Design a security architecture for a hotel in Bali with a public booking website, staff PCs, a payments system and guest Wi-Fi, explaining where firewalls, a DMZ, a proxy and an IDS/IPS would be placed and why.', 'Perimeter firewall to the internet; web server in a DMZ between two firewalls; staff LAN and payments system in separate internal segments with strict rules (payments isolated for PCI DSS); guest Wi-Fi on its own VLAN with internet-only access; proxy for staff web access with filtering/logging; IDS/IPS monitoring DMZ and internal traffic; default-deny rules and logging.', 6)],
))


def _fw_match(rule, pkt):
    act, proto, src, dport = rule
    if proto != 'any' and proto != pkt['proto']:
        return False
    if src != 'any' and ipaddress.ip_address(pkt['src']) not in ipaddress.ip_network(src):
        return False
    if dport != 'any' and dport != pkt['dport']:
        return False
    return True


@R.add('ch07-st2', 'C3', (2, 5), 'short')
def firewall_rules(rng, slot):
    bad = rng.choice(['203.0.113.0/24', '198.51.100.0/24'])
    rules = [('DENY', 'any', bad, 'any'), ('ALLOW', 'TCP', 'any', 443), ('ALLOW', 'TCP', '10.0.0.0/8', 22),
             ('ALLOW', 'UDP', 'any', 53), ('DENY', 'any', 'any', 'any')]
    if rng.random() < 0.5:
        rules[0], rules[1] = rules[1], rules[0]
    pkts = []
    for _ in range(3 if slot.d <= 3 else 4):
        src = rng.choice([bad.replace('0/24', str(rng.randint(1, 254))), f'10.{rng.randint(0, 9)}.{rng.randint(0, 9)}.{rng.randint(1, 254)}', f'{rng.randint(11, 99)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}'])
        proto, dport = rng.choice([('TCP', 443), ('TCP', 22), ('UDP', 53), ('TCP', 80), ('TCP', 3389)])
        pkts.append(dict(src=src, proto=proto, dport=dport))
    res = []
    for p in pkts:
        for i, r in enumerate(rules, 1):
            if _fw_match(r, p):
                res.append(f'{p["proto"]} from {p["src"]} to port {p["dport"]}: {r[0]} (rule {i})')
                break
    rt = '\n'.join(f'{i}. {a} {pr} from {s} to port {d}' for i, (a, pr, s, d) in enumerate(rules, 1))
    return dict(stem=f'A packet-filtering firewall applies these rules in order, using the first rule that matches:\n{rt}\nState whether each packet is allowed or denied, and which rule decides it: ' + '; '.join(f'({chr(97 + i)}) {p["proto"]} from {p["src"]} to port {p["dport"]}' for i, p in enumerate(pkts)) + '.',
                answer='; '.join(res), markingKey='1 mark each: ' + '; '.join(res) + '. (First matching rule applies; rule order matters.)', marks=len(pkts))


@R.add('ch07-st2', 'C3', (2, 5), 'short')
def ids_threshold(rng, slot):
    ips = [f'198.51.100.{rng.randint(1, 254)}' for _ in range(3)]
    thr = rng.choice([3, 4, 5])
    win = rng.choice([60, 120])
    events = []
    for ip in ips:
        k = rng.randint(1, thr + 3)
        t0 = rng.randint(0, 200)
        gap = rng.choice([5, 10, 20, 40])
        events += [(t0 + i * gap, ip) for i in range(k)]
    events.sort()
    flagged = []
    for ip in ips:
        ts = [t for t, i in events if i == ip]
        if any(sum(1 for u in ts if t <= u < t + win) >= thr for t in ts):
            flagged.append(ip)
    log = ', '.join(f'{t}s {ip}' for t, ip in events)
    return dict(stem=f'An IDS raises an alert when one IP address has {thr} or more failed log-ins within any {win}-second window. The failed log-ins (time, source) are: {log}. Which IP addresses trigger an alert?',
                answer=', '.join(flagged) or 'None', markingKey=f'Count failures per IP within a sliding {win}-s window: alerts for {", ".join(flagged) or "none"} (1 mark per correct IP, 1 for correctly excluding the others).', marks=3)


K.ar('ch07-st2', [
    ('Specific firewall rules should be placed above general rules.', 'Firewalls apply the first rule that matches a packet.', 0, 'Both true; R explains A.'),
    ('An IDS blocks malicious traffic automatically.', 'An IDS monitors traffic for suspicious patterns.', 3, 'A false (that is an IPS); R true.'),
    ('Public web servers are often placed in a DMZ.', 'A compromised server in a DMZ does not give direct access to the internal network.', 0, 'Both true; R explains A.'),
])


R.facts('ch07-st3', F(
    terms=[('encryption', 'transforming plaintext into ciphertext using an algorithm and a key so that only someone with the correct key can read it'),
           ('symmetric encryption', 'encryption in which the same secret key is used to encrypt and decrypt, e.g. AES'),
           ('asymmetric encryption', 'encryption that uses a key pair: data encrypted with the public key can only be decrypted with the matching private key, e.g. RSA'),
           ('plaintext', 'the original, readable data before encryption'),
           ('ciphertext', 'the scrambled data produced by encryption'),
           ('key exchange', 'the process of securely sharing a symmetric key, often by using asymmetric encryption or Diffie-Hellman'),
           ('Caesar cipher', 'a substitution cipher in which each letter is shifted a fixed number of places along the alphabet')],
    facts=[('In asymmetric encryption, which key does a sender use to encrypt a message for Priya?', 'Priya\'s public key', ['Priya\'s private key', 'The sender\'s private key', 'A key shared on a sticky note'], 'Only Priya\'s private key can then decrypt it.'),
           ('Why is symmetric encryption used for bulk data in HTTPS?', 'It is much faster than asymmetric encryption', ['It needs no key', 'It is impossible to break', 'It uses longer keys'], 'Asymmetric encryption is used only to establish the session key.'),
           ('How many possible keys does the Caesar cipher (English alphabet) have?', '25 useful shifts', ['26 factorial', '2^128', '1000'], 'Only 25 non-trivial shifts – trivially brute-forced.'),
           ('Which is a symmetric algorithm?', 'AES', ['RSA', 'Elliptic-curve Diffie-Hellman', 'SHA-256'], 'AES uses the same key for both operations; SHA-256 is a hash.')],
    why=[('Explain why asymmetric encryption solves the key distribution problem.', 'The public key can be shared openly; anyone can encrypt with it but only the holder of the private key can decrypt, so no secret key ever needs to be sent over an insecure channel.'),
         ('Explain why HTTPS uses both asymmetric and symmetric encryption.', 'Asymmetric encryption (or key exchange) securely establishes a shared session key without prior secrets, then fast symmetric encryption protects the bulk data; this combines security of key exchange with speed.'),
         ('Explain why longer keys make encryption more secure.', 'Each extra bit doubles the number of possible keys, so a brute-force search becomes exponentially longer; 128-bit keys give 2^128 possibilities, far beyond any feasible search.')],
    contrast=[('symmetric encryption', 'asymmetric encryption', 'Symmetric encryption uses one shared secret key for encryption and decryption (fast, but the key must be distributed securely); asymmetric uses a public/private key pair (solves key distribution and enables signatures, but is much slower).'),
              ('encryption', 'hashing', 'Encryption is reversible with the correct key and protects confidentiality; hashing is a one-way function producing a fixed-length digest used to check integrity or store passwords.')],
    misc=[('In public-key encryption, messages are encrypted with the recipient\'s private key.', 'Messages for confidentiality are encrypted with the recipient\'s public key; the private key decrypts (private keys are used for signing).'),
          ('Encryption stops attackers from intercepting data.', 'Encrypted data can still be intercepted; encryption makes it unreadable without the key.'),
          ('The Caesar cipher is secure if the shift is kept secret.', 'With only 25 shifts it can be broken instantly by trying them all or by frequency analysis.')],
    evaluate=[('Strong encryption should have a "backdoor" for law enforcement.', ['helps investigate serious crime and terrorism'], ['a backdoor can be found and abused by criminals or hostile states', 'undermines trust in secure communications and commerce', 'criminals can use other, backdoor-free tools'], 'Most security experts argue backdoors weaken security for everyone; the balance between privacy and investigation remains contested.')],
    extended=[('Explain, step by step, how Sofia can send a confidential file to Kenji over the internet using a hybrid of symmetric and asymmetric encryption, and explain why the file remains confidential even if all traffic is intercepted.', 'Sofia generates a random AES session key; encrypts the file with AES (fast); encrypts the AES key with Kenji\'s public RSA key; sends both. Kenji decrypts the AES key with his private key, then decrypts the file. An interceptor has only ciphertext and the encrypted key; without Kenji\'s private key they cannot recover the AES key, and brute-forcing a 128/256-bit key is infeasible.', 6)],
))


def _caesar(s, k):
    return ''.join(chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c for c in s.upper())


@R.add('ch07-st3', 'C3', (1, 4), 'short')
def caesar(rng, slot):
    words = ['ATTACK AT DAWN', 'NETWORK SECURE', 'MEET AT NOON', 'PASSWORD RESET', 'ROUTER DOWN', 'SEND THE KEY', 'FIREWALL ON', 'DATA PACKET']
    p = rng.choice(words)
    k = rng.randint(1, 25)
    c = _caesar(p, k)
    if rng.random() < 0.5:
        return dict(stem=f'Encrypt "{p}" using a Caesar cipher with a shift of {k} to the right.', answer=c, markingKey=f'{c} (2 marks; 1 if one or two letters wrong). Spaces unchanged.', marks=2)
    return dict(stem=f'The ciphertext "{c}" was produced by a Caesar cipher with a right shift of {k}. Decrypt it and explain why this cipher is insecure.', answer=f'{p}; only 25 possible shifts so it can be brute-forced (or broken by frequency analysis)',
                markingKey=f'{p} (2); weakness – tiny key space / letter frequencies preserved (1).', marks=3)


@R.add('ch07-st3', 'C3', (2, 5), 'short')
def xor_cipher(rng, slot):
    word = rng.choice(['HI', 'OK', 'IB', 'NET', 'KEY'])[: 2 if slot.d <= 3 else 3]
    key = rng.randint(1, 255)
    pt = [ord(c) for c in word]
    ct = [b ^ key for b in pt]
    return dict(stem=f'A simple symmetric cipher XORs each 8-bit ASCII code with the key {format(key, "08b")}. Encrypt "{word}" (ASCII codes {", ".join(map(str, pt))}) and show that XORing the ciphertext with the same key restores the plaintext.',
                answer=' '.join(format(b, '08b') for b in ct), markingKey=' | '.join(f'{format(a, "08b")} XOR {format(key, "08b")} = {format(b, "08b")}' for a, b in zip(pt, ct)) + '. Decryption: (P XOR K) XOR K = P because K XOR K = 0 (1 mark).', marks=3)


@R.add('ch07-st3', 'C3', (3, 5), 'numerical')
def rsa_small(rng, slot):
    p, q = rng.choice([(5, 11), (7, 11), (3, 17), (5, 13), (11, 13), (7, 13)])
    n, phi = p * q, (p - 1) * (q - 1)
    e = next(x for x in [3, 5, 7, 11, 13, 17] if math.gcd(x, phi) == 1)
    d = pow(e, -1, phi)
    m = rng.randint(2, n - 2)
    c = pow(m, e, n)
    if c == m:
        return None
    return dict(stem=f'In a toy RSA system p = {p} and q = {q}, and the public exponent is e = {e}. Calculate n, φ(n) and the private exponent d, then encrypt the message m = {m} and verify that decryption returns m.',
                answer=f'n = {n}, φ = {phi}, d = {d}; c = {c}; c^d mod n = {pow(c, d, n)}',
                markingKey=f'n = {p}×{q} = {n} (A1); φ = {p - 1}×{q - 1} = {phi} (A1); d = e⁻¹ mod φ = {d} since {e}×{d} = {e * d} ≡ 1 (mod {phi}) (M1 A1); c = {m}^{e} mod {n} = {c} (A1); {c}^{d} mod {n} = {m} (R1).', marks=6)


@R.add('ch07-st3', 'C3', (2, 4), 'numerical')
def key_count(rng, slot):
    n = rng.choice([5, 10, 20, 50, 100, 1000])
    return dict(stem=f'{n} people each need to communicate privately with every other person. Calculate the number of keys needed using symmetric encryption (one shared key per pair) and using asymmetric encryption (one key pair per person).',
                answer=f'Symmetric {n * (n - 1) // 2} keys; asymmetric {2 * n} keys ({n} pairs)', markingKey=f'n(n − 1)/2 = {n * (n - 1) // 2} (M1 A1); 2n = {2 * n} (A1); asymmetric scales far better.', marks=3)


K.ar('ch07-st3', [
    ('Asymmetric encryption is slower than symmetric encryption.', 'Asymmetric algorithms rely on computationally expensive operations on very large numbers.', 0, 'Both true; R explains A.'),
    ('A public key must be kept secret.', 'A message encrypted with a public key can only be decrypted with the matching private key.', 3, 'A false – public keys are shared openly; R true.'),
    ('The Caesar cipher is easily broken.', 'It has only 25 possible keys.', 0, 'Both true; R explains A.'),
])


R.facts('ch07-st4', F(
    terms=[('hash function', 'a one-way function that maps data of any size to a fixed-length digest, where a small change in input produces a completely different output'),
           ('digital signature', 'a hash of a message encrypted with the sender\'s private key, which the receiver verifies with the sender\'s public key to prove authenticity and integrity'),
           ('digital certificate', 'an electronic document issued by a certificate authority that binds a public key to the identity of its owner'),
           ('certificate authority (CA)', 'a trusted organisation that verifies identities and issues and signs digital certificates'),
           ('salt', 'random data added to a password before hashing so that identical passwords produce different hashes and precomputed tables are useless'),
           ('non-repudiation', 'assurance that the sender of a signed message cannot later deny having sent it'),
           ('TLS', 'Transport Layer Security, the protocol that uses certificates and encryption to secure connections such as HTTPS')],
    facts=[('Which key is used to create a digital signature?', 'The sender\'s private key', ['The sender\'s public key', 'The receiver\'s public key', 'A shared symmetric key'], 'Only the sender can sign; anyone can verify with the public key.'),
           ('Why are passwords stored as salted hashes rather than encrypted?', 'Hashes cannot be reversed, so a stolen database does not reveal the passwords', ['Hashes are shorter to type', 'Encryption is illegal for passwords', 'Hashing makes log-in faster than encryption'], 'The system only needs to compare hashes.'),
           ('A browser shows a warning that a site\'s certificate has expired. What has the browser checked?', 'The certificate\'s validity dates', ['The site\'s IP address', 'The page\'s HTML', 'The user\'s password'], 'Expired certificates are no longer trusted.'),
           ('What length is a SHA-256 digest?', '256 bits (64 hex digits)', ['Same length as the input', '56 bits', '1024 bits'], 'Hash output length is fixed.')],
    why=[('Explain how a digital signature proves that a message has not been altered.', 'The receiver decrypts the signature with the sender\'s public key to get the original hash and hashes the received message; if the two hashes match, the message is unchanged, because any change would produce a different hash.'),
         ('Explain why a browser trusts a website\'s certificate.', 'The certificate is signed by a certificate authority whose root certificate is pre-installed in the browser/OS; the browser verifies the chain of signatures, the domain name and validity dates, so it trusts that the public key belongs to the site.'),
         ('Explain why salting passwords defeats rainbow-table attacks.', 'A rainbow table stores precomputed hashes of common passwords; a unique random salt per user changes every hash, so the table would have to be recomputed for each salt, which is infeasible.')],
    contrast=[('a digital signature', 'a digital certificate', 'A digital signature is created by a sender with their private key to authenticate a specific message; a certificate is issued by a CA to bind a public key to an identity so others can trust that key.'),
              ('hashing', 'encryption', 'Hashing is one-way and produces a fixed-size digest for integrity checking; encryption is two-way, using a key to make data confidential and recoverable.')],
    misc=[('Hashing a password twice makes it possible to decrypt it.', 'Hashes are one-way; repeated hashing (key stretching) makes guessing slower but never allows reversal.'),
          ('A padlock icon proves that a website is honest.', 'The padlock shows the connection is encrypted and the certificate is valid for the domain; phishing sites can also obtain certificates.'),
          ('Digital signatures keep the message content secret.', 'Signatures provide authenticity and integrity; the message itself is not encrypted unless encryption is also used.')],
    evaluate=[('Digital certificates make online transactions completely trustworthy.', ['authenticate servers and enable encrypted TLS', 'CAs verify domain ownership'], ['CAs can be compromised or mis-issue certificates', 'domain-validated certificates do not prove the organisation is honest', 'users ignore warnings'], 'Certificates greatly increase trust in identity and confidentiality, but do not guarantee honesty.')],
    extended=[('Describe the full process by which an e-commerce site\'s server proves its identity to a customer\'s browser and establishes a secure connection, with reference to certificates, CAs, public/private keys, hashing and session keys.', 'Browser connects; server sends its certificate (public key, domain, validity, CA signature). Browser verifies the CA signature using the CA\'s public key (chain of trust to a root), checks domain and dates/revocation. Key exchange (e.g. ECDHE, authenticated by the server\'s private key signature) produces a shared session key; data is then encrypted symmetrically (AES) with message authentication (hash-based MAC) to ensure integrity.', 6)],
))


@R.add('ch07-st4', 'C3', (2, 5), 'short')
def hash_check(rng, slot):
    pw = rng.choice(['sunflower7', 'Lima2026!', 'blue-otter', 'qwerty123', 'Tr0ub4dor', 'MangoTree', 'kibera99'])
    salt = ''.join(rng.choice('0123456789abcdef') for _ in range(4))
    stored = hashlib.sha256((salt + pw).encode()).hexdigest()[:12]
    cands = rng.sample(['sunflower7', 'Lima2026!', 'blue-otter', 'qwerty123', 'Tr0ub4dor', 'MangoTree', 'kibera99', 'Sunflower7'], 3)
    if pw not in cands:
        cands[rng.randrange(3)] = pw
    rows = '; '.join(f'"{c}" → {hashlib.sha256((salt + c).encode()).hexdigest()[:12]}' for c in cands)
    return dict(stem=f'A system stores the salt "{salt}" and the first 12 hex digits of SHA-256(salt + password): {stored}. The truncated hashes of three candidate log-in attempts are: {rows}. Which attempt is accepted, and why does the system never need to store the password itself?',
                answer=f'"{pw}"; the system hashes the attempt with the salt and compares digests, so only the hash is stored',
                markingKey=f'"{pw}" matches {stored} (1); explanation: hash the entered password with the stored salt and compare; hashes cannot be reversed so the password is never stored (2).', marks=3)


@R.add('ch07-st4', 'C3', (2, 4), 'short')
def avalanche(rng, slot):
    a = rng.choice(['Pay Kenji 100', 'Transfer 500 to Omar', 'Order 12 laptops', 'Grade: 6', 'Approve invoice 3471'])
    i = max(i for i, ch in enumerate(a) if ch.isdigit())
    b = a[:i] + str((int(a[i]) + 1) % 10) + a[i + 1:]
    ha, hb = hashlib.sha256(a.encode()).hexdigest()[:16], hashlib.sha256(b.encode()).hexdigest()[:16]
    same = sum(x == y for x, y in zip(ha, hb))
    return dict(stem=f'The first 16 hex digits of SHA-256("{a}") are {ha} and of SHA-256("{b}") are {hb}. Explain what this shows about hash functions and why it makes hashes useful for detecting tampering.',
                answer='A one-character change produces a completely different digest (avalanche effect), so any alteration of a signed or checksummed message is detected.',
                markingKey=f'Only {same} of 16 positions coincide by chance (1); avalanche effect (1); a recomputed hash will not match if data is altered, so integrity can be verified (1).', marks=3)


@R.add('ch07-st4', 'C3', (2, 5), 'short')
def cert_check(rng, slot):
    import datetime as _d
    today = _d.date(2026, 11, 18)
    cases = []
    for _ in range(3):
        dom = rng.choice(['shop.example.com', 'bank.example.org', 'mail.example.net'])
        req = dom if rng.random() < 0.7 else 'www.' + dom.split('.', 1)[1]
        start = today - _d.timedelta(days=rng.randint(10, 400))
        end = start + _d.timedelta(days=rng.choice([90, 365, 398]))
        trusted = rng.random() < 0.75
        probs = []
        if req != dom:
            probs.append('name mismatch')
        if end < today:
            probs.append('expired')
        if not trusted:
            probs.append('issuer not a trusted CA (self-signed)')
        cases.append((req, dom, start, end, trusted, probs))
    lines = '; '.join(f'({chr(97 + i)}) visiting {r}: certificate for {d}, valid {s} to {e}, issued by {"a trusted CA" if t else "itself"}' for i, (r, d, s, e, t, p) in enumerate(cases))
    ans = '; '.join(f'({chr(97 + i)}) {"accepted" if not p else "warning – " + ", ".join(p)}' for i, (r, d, s, e, t, p) in enumerate(cases))
    return dict(stem=f'Today is {today}. A browser checks each certificate\'s domain name, validity dates and issuer. State whether each is accepted or produces a warning, giving the reason: {lines}.',
                answer=ans, markingKey=f'1 mark each: {ans}.', marks=3)


K.ar('ch07-st4', [
    ('A digital signature provides non-repudiation.', 'Only the sender holds the private key used to create the signature.', 0, 'Both true; R explains A.'),
    ('Hashed passwords can be decrypted by the system administrator.', 'Hash functions are one-way.', 3, 'A false; R true and is why.'),
    ('Browsers trust certificates signed by root CAs in their trust store.', 'Root CA certificates are pre-installed with the browser or operating system.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# Theme B helpers: small algorithms written in pseudocode with an executable Python twin
# =============================================================================================
def _alg_digit_sum(rng):
    x = rng.randint(1000, 99999)
    pseudo = f'X ← {x}\nS ← 0\nloop while X > 0\n    S ← S + X mod 10\n    X ← X div 10\nend loop\noutput S'
    rows, X, S = [], x, 0
    while X > 0:
        S += X % 10; X //= 10; rows.append((X, S))
    return pseudo, str(S), ['X', 'S'], rows


def _alg_product(rng):
    n = rng.randint(4, 7)
    a = rng.randint(1, 3)
    pseudo = f'P ← 1\nloop I from {a} to {n}\n    P ← P * I\nend loop\noutput P'
    rows, P = [], 1
    for I in range(a, n + 1):
        P *= I; rows.append((I, P))
    return pseudo, str(P), ['I', 'P'], rows


def _alg_gcd(rng):
    a, b = rng.randint(30, 300), rng.randint(10, 120)
    pseudo = f'A ← {a}\nB ← {b}\nloop while B ≠ 0\n    R ← A mod B\n    A ← B\n    B ← R\nend loop\noutput A'
    rows, A, B = [], a, b
    while B != 0:
        R = A % B; A = B; B = R; rows.append((R, A, B))
    return pseudo, str(A), ['R', 'A', 'B'], rows


def _alg_binary(rng):
    n = rng.randint(9, 120)
    pseudo = f'N ← {n}\nB ← ""\nloop while N > 0\n    B ← (N mod 2) + B    // join as text\n    N ← N div 2\nend loop\noutput B'
    rows, N, B = [], n, ''
    while N > 0:
        B = str(N % 2) + B; N //= 2; rows.append((N, B))
    return pseudo, B, ['N', 'B'], rows


def _alg_count_mult(rng):
    a, b, k = rng.randint(1, 10), rng.randint(15, 30), rng.randint(3, 6)
    pseudo = f'C ← 0\nloop I from {a} to {b}\n    if I mod {k} = 0 then\n        C ← C + 1\n    end if\nend loop\noutput C'
    rows, C = [], 0
    for I in range(a, b + 1):
        if I % k == 0:
            C += 1
            rows.append((I, C))
    return pseudo, str(C), ['I (when C changes)', 'C'], rows


def _alg_fib(rng):
    n = rng.randint(5, 9)
    pseudo = f'A ← 0\nB ← 1\nloop K from 1 to {n}\n    T ← A + B\n    A ← B\n    B ← T\nend loop\noutput A'
    rows, A, B = [], 0, 1
    for K in range(1, n + 1):
        T = A + B; A = B; B = T; rows.append((K, T, A, B))
    return pseudo, str(A), ['K', 'T', 'A', 'B'], rows


def _alg_max(rng):
    arr = [rng.randint(-20, 60) for _ in range(rng.randint(5, 7))]
    pseudo = f'ARR ← {arr}\nM ← ARR[0]\nP ← 0\nloop I from 1 to {len(arr) - 1}\n    if ARR[I] > M then\n        M ← ARR[I]\n        P ← I\n    end if\nend loop\noutput M, P'
    rows, M, P = [], arr[0], 0
    for I in range(1, len(arr)):
        if arr[I] > M:
            M = arr[I]; P = I
        rows.append((I, M, P))
    return pseudo, f'{M}, {P}', ['I', 'M', 'P'], rows


def _alg_reverse(rng):
    x = rng.randint(1200, 98765)
    pseudo = f'X ← {x}\nR ← 0\nloop while X > 0\n    R ← R * 10 + X mod 10\n    X ← X div 10\nend loop\noutput R'
    rows, X, R = [], x, 0
    while X > 0:
        R = R * 10 + X % 10; X //= 10; rows.append((X, R))
    return pseudo, str(R), ['X', 'R'], rows


def _alg_nested(rng):
    n = rng.randint(3, 5)
    pseudo = f'T ← 0\nloop I from 1 to {n}\n    loop J from 1 to I\n        T ← T + J\n    end loop\nend loop\noutput T'
    rows, T = [], 0
    for I in range(1, n + 1):
        for J in range(1, I + 1):
            T += J
        rows.append((I, T))
    return pseudo, str(T), ['I (end of inner loop)', 'T'], rows


def _alg_collatz(rng):
    n = rng.choice([6, 7, 9, 11, 12, 13, 15, 17, 19])
    pseudo = f'N ← {n}\nS ← 0\nloop while N ≠ 1\n    if N mod 2 = 0 then\n        N ← N div 2\n    else\n        N ← 3 * N + 1\n    end if\n    S ← S + 1\nend loop\noutput S'
    rows, N, S = [], n, 0
    while N != 1:
        N = N // 2 if N % 2 == 0 else 3 * N + 1
        S += 1; rows.append((N, S))
    return pseudo, str(S), ['N', 'S'], rows


def _alg_running_avg(rng):
    marks = [rng.randint(35, 99) for _ in range(rng.randint(4, 6))]
    th = rng.choice([50, 60, 70])
    pseudo = f'MARKS ← {marks}\nTOTAL ← 0\nPASS ← 0\nloop I from 0 to {len(marks) - 1}\n    TOTAL ← TOTAL + MARKS[I]\n    if MARKS[I] >= {th} then\n        PASS ← PASS + 1\n    end if\nend loop\noutput TOTAL / {len(marks)}, PASS'
    rows, T, P = [], 0, 0
    for I, m_ in enumerate(marks):
        T += m_
        if m_ >= th:
            P += 1
        rows.append((I, T, P))
    return pseudo, f'{r2(T / len(marks))}, {P}', ['I', 'TOTAL', 'PASS'], rows


ALGS = [_alg_digit_sum, _alg_product, _alg_gcd, _alg_binary, _alg_count_mult, _alg_fib, _alg_max, _alg_reverse, _alg_nested, _alg_collatz, _alg_running_avg]
_ALG_PURPOSE = {'_alg_digit_sum': 'adds the digits of X', '_alg_product': 'multiplies the integers in the range', '_alg_gcd': 'finds the greatest common divisor (Euclid\'s algorithm)',
                '_alg_binary': 'converts N to a binary string', '_alg_count_mult': 'counts the multiples in the range', '_alg_fib': 'finds a Fibonacci number',
                '_alg_max': 'finds the largest value and its index', '_alg_reverse': 'reverses the digits of X', '_alg_nested': 'sums triangular numbers',
                '_alg_collatz': 'counts the steps of the Collatz sequence to reach 1', '_alg_running_avg': 'calculates the mean mark and the number of passes'}


# =============================================================================================
# ch08 B1.1 Computational thinking
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('decomposition', 'breaking a complex problem down into smaller, more manageable sub-problems that can be solved separately'),
           ('pattern recognition', 'identifying similarities, trends or repeated elements within or between problems so that common solutions can be reused'),
           ('abstraction', 'removing unnecessary detail and focusing on the essential features of a problem in order to model it'),
           ('algorithm', 'a finite, ordered sequence of unambiguous instructions that solves a problem or completes a task'),
           ('algorithmic thinking', 'designing a clear, step-by-step solution that can be followed by a computer or a person'),
           ('generalisation', 'adapting a solution so that it works for a whole class of similar problems rather than one specific case')],
    facts=[('A London Underground map shows stations and connections but not exact distances. This is an example of…', 'abstraction', ['decomposition', 'pattern recognition', 'iteration'], 'Irrelevant geographical detail is removed.'),
           ('Splitting "build a school website" into login, timetable, news and contact pages is…', 'decomposition', ['abstraction', 'encryption', 'compilation'], 'The large problem is broken into sub-problems.'),
           ('Which is NOT a property of a good algorithm?', 'It may run forever on some inputs', ['It is unambiguous', 'It has a finite number of steps', 'It produces the correct output for valid inputs'], 'An algorithm must terminate.'),
           ('Noticing that calculating pay for every employee uses the same steps is an example of…', 'pattern recognition', ['abstraction', 'decomposition', 'validation'], 'The repeated pattern can become one reusable routine.')],
    why=[('Explain why decomposition makes a large programming project easier to manage.', 'Each sub-problem is small enough to understand, design, code and test independently; tasks can be shared among team members, and modules can be reused and debugged in isolation.'),
         ('Explain why abstraction is essential when creating a computer model of a real system.', 'Real systems contain far more detail than can be represented or computed; abstraction keeps only the features that affect the result, making the model simpler, faster to build and easier to understand.'),
         ('Explain how pattern recognition leads to more efficient code.', 'Recognising that steps repeat lets the programmer write them once – as a loop or a reusable function with parameters – rather than duplicating code, which reduces errors and simplifies maintenance.')],
    contrast=[('decomposition', 'abstraction', 'Decomposition splits a problem into smaller parts; abstraction removes unnecessary details to focus on what matters. They are often used together.'),
              ('an algorithm', 'a program', 'An algorithm is a language-independent sequence of steps to solve a problem; a program is an implementation of an algorithm in a specific programming language that a computer can execute.')],
    misc=[('Abstraction means making a problem more complicated so that it is more realistic.', 'Abstraction means hiding or removing unnecessary detail to simplify the problem.'),
          ('An algorithm must be written in a programming language.', 'Algorithms can be expressed in pseudocode, flowcharts or structured English; a program is the coded form.'),
          ('Decomposition is only useful for very large problems.', 'Even small problems benefit from breaking them into steps (input, process, output) that can be tested separately.')],
    evaluate=[('Computational thinking is only useful for computer scientists.', ['it underpins programming and system design'], ['decomposition, abstraction and pattern recognition are used in science, business planning, medicine and everyday problem solving'], 'Computational thinking is a general problem-solving approach valuable far beyond computer science.')],
    extended=[('A city council in Medellín wants an app to help residents plan journeys combining buses, metro and cable cars. Apply decomposition, pattern recognition and abstraction to the design of this app.', 'Decomposition: route finding, timetable data, user interface, ticket pricing, real-time updates, accessibility. Pattern recognition: each transport mode is a network of stops and connections with times – one graph model; journey cost follows the same calculation per leg. Abstraction: represent stops as nodes and connections as weighted edges (time, cost), ignoring street detail, vehicle type or exact geography; keep only data relevant to planning.', 6)],
))


@R.add('ch08-st1', 'C3', (1, 4), 'short')
def ct_identify(rng, slot):
    items = [('A weather app shows only temperature, rain chance and wind for each hour, ignoring air pressure details.', 'abstraction'),
             ('A team splits a library system into loans, catalogue search, member accounts and fines.', 'decomposition'),
             ('A programmer notices that validating email, phone and postcode fields all follow "check format, show error, re-ask".', 'pattern recognition'),
             ('A game designer represents a city as a grid of squares, each either road, building or park.', 'abstraction'),
             ('A recipe app breaks "cook dinner" into shopping list, preparation steps and cooking timers.', 'decomposition'),
             ('A student realises that calculating the area of every room uses the same length × width steps and writes one function.', 'pattern recognition / generalisation'),
             ('A metro map draws all lines as straight segments at 45° angles.', 'abstraction'),
             ('An engineer writes precise numbered steps for resetting a router so that anyone can follow them.', 'algorithm design')]
    s = rng.sample(items, 3)
    ans = '; '.join(f'({chr(97 + i)}) {b}' for i, (a, b) in enumerate(s))
    return dict(stem='Identify the computational thinking concept that is mainly shown in each case: ' + ' '.join(f'({chr(97 + i)}) {a}' for i, (a, b) in enumerate(s)), answer=ans,
                markingKey=f'1 mark each: {ans}.', marks=3)


@R.add('ch08-st1', 'C3', (2, 5), 'short')
def pattern_seq(rng, slot):
    kind = rng.choice(['arith', 'geom', 'square', 'tri'])
    a, d = rng.randint(2, 9), rng.randint(2, 7)
    if kind == 'arith':
        seq = [a + d * i for i in range(5)]; rule = f'T(n) = {a} + {d}(n − 1)'; f = lambda n: a + d * (n - 1)
    elif kind == 'geom':
        d = rng.choice([2, 3]); seq = [a * d ** i for i in range(5)]; rule = f'T(n) = {a} × {d}^(n − 1)'; f = lambda n: a * d ** (n - 1)
    elif kind == 'square':
        seq = [i * i + a for i in range(1, 6)]; rule = f'T(n) = n² + {a}'; f = lambda n: n * n + a
    else:
        seq = [i * (i + 1) // 2 for i in range(1, 6)]; rule = 'T(n) = n(n + 1)/2'; f = lambda n: n * (n + 1) // 2
    k = rng.choice([10, 12, 15, 20])
    return dict(stem=f'A loop produces the values {", ".join(map(str, seq))}, … Use pattern recognition to give a general rule for the n-th value and state the {k}th value. Explain how generalising the rule helps the programmer.',
                answer=f'{rule}; T({k}) = {f(k)}', markingKey=f'Rule {rule} (2); T({k}) = {f(k)} (1); a general formula/function works for any n, avoiding special-case code (1).', marks=4)


K.ar('ch08-st1', [
    ('Abstraction simplifies the design of a model.', 'Abstraction removes details that are not relevant to the problem.', 0, 'Both true; R explains A.'),
    ('Decomposition makes it easier to test a program.', 'Each sub-problem can be tested separately.', 0, 'Both true; R explains A.'),
    ('An algorithm may contain ambiguous steps if a human will follow it.', 'Algorithms can be written in pseudocode.', 3, 'A false – an algorithm must be unambiguous; R true.'),
])


R.facts('ch08-st2', F(
    terms=[('flowchart', 'a diagram that represents an algorithm using standard symbols connected by arrows showing the flow of control'),
           ('pseudocode', 'a structured, language-independent way of describing an algorithm using English-like statements and programming constructs'),
           ('decision symbol', 'the diamond-shaped flowchart symbol for a yes/no question, with one arrow leaving for each outcome'),
           ('terminator', 'the rounded flowchart symbol that marks the start or end of an algorithm'),
           ('sequence', 'the control structure in which instructions are executed one after another in order'),
           ('selection', 'the control structure in which a condition decides which of two or more paths is followed'),
           ('iteration', 'the control structure in which a group of instructions is repeated, either a fixed number of times or while a condition holds')],
    facts=[('Which flowchart symbol is used for input and output?', 'Parallelogram', ['Diamond', 'Rectangle', 'Oval'], 'Parallelograms show input/output.'),
           ('Which flowchart symbol represents a process such as X ← X + 1?', 'Rectangle', ['Diamond', 'Parallelogram', 'Circle'], 'Rectangles show processes.'),
           ('In a flowchart, a loop is shown by…', 'an arrow returning to an earlier point, controlled by a decision', ['a double rectangle', 'a dotted line', 'two terminators'], 'Iteration is drawn with a back-arrow from a decision.'),
           ('Why is pseudocode used in exams instead of a specific language?', 'It focuses on the logic of the algorithm, independent of language syntax', ['It runs faster', 'It can be compiled directly', 'It needs no variables'], 'Language-independence lets any programmer read it.')],
    why=[('Explain why programmers design algorithms with flowcharts or pseudocode before coding.', 'It lets them plan and check the logic without worrying about syntax, communicate the design to others, spot errors early (cheaper to fix), and then translate the design into any language.'),
         ('Explain why a decision symbol must have exactly one entry and two (or more) labelled exits.', 'The condition evaluates to a single outcome, so the flow must continue along exactly one clearly labelled path; unlabelled or missing exits would make the algorithm ambiguous.'),
         ('Explain why a while loop is more appropriate than a count-controlled loop when validating user input.', 'The number of attempts is not known in advance; a while loop repeats until a valid value is entered, whereas a count-controlled loop runs a fixed number of times.')],
    contrast=[('a flowchart', 'pseudocode', 'A flowchart shows an algorithm graphically with symbols and arrows (easy to see the flow); pseudocode writes it as structured text (more compact, closer to code, easier to edit).'),
              ('selection', 'iteration', 'Selection chooses between paths based on a condition (if/else); iteration repeats a block of instructions (loops).')],
    misc=[('A flowchart decision box can have only a "yes" exit.', 'A decision must have an exit for each possible outcome, e.g. both yes and no.'),
          ('Pseudocode has a strict syntax that must be followed exactly or it will not run.', 'Pseudocode is not executed; it must be clear and consistent, but small syntax variations are acceptable.'),
          ('A loop in a flowchart is drawn using a special loop symbol.', 'Loops are shown with a decision and an arrow returning to an earlier step.')],
    evaluate=[('Flowcharts are better than pseudocode for designing algorithms.', ['visual flow is easy for beginners and non-programmers', 'good for showing branching'], ['large algorithms become sprawling and hard to edit', 'pseudocode is closer to real code and quicker to write'], 'Flowcharts suit small algorithms and communication; pseudocode scales better for larger designs.')],
    extended=[('Design, in pseudocode, an algorithm that reads the ages of visitors to a museum until −1 is entered, then outputs the number of child (under 12), adult and senior (65+) visitors and the total ticket income (child 5, adult 15, senior 8). Explain how your algorithm uses sequence, selection and iteration.', 'Initialise counters C, A, S ← 0; input AGE; loop while AGE ≠ −1: if AGE < 12 then C ← C + 1 else if AGE >= 65 then S ← S + 1 else A ← A + 1 end if; input AGE; end loop; output C, A, S, 5C + 15A + 8S. Sequence: initialisation then loop then output; selection: classifying each age; iteration: the sentinel-controlled loop.', 6)],
))


def _flow_grade(rng):
    a, b = rng.choice([(50, 70), (40, 65), (55, 80)])
    x = rng.randint(20, 99)
    out = 'Merit' if x >= b else 'Pass' if x >= a else 'Fail'
    desc = (f'START → INPUT SCORE → decision "SCORE >= {b}?" – Yes: OUTPUT "Merit" → END; No: decision "SCORE >= {a}?" – Yes: OUTPUT "Pass" → END; No: OUTPUT "Fail" → END')
    return desc, f'SCORE = {x}', out


def _flow_loop(rng):
    n = rng.randint(3, 6)
    s = rng.randint(1, 4)
    total, i = 0, 1
    while i <= n:
        total += s * i
        i += 1
    desc = f'START → T ← 0, I ← 1 → decision "I <= {n}?" – Yes: T ← T + {s} × I, I ← I + 1, return to the decision; No: OUTPUT T → END'
    return desc, 'no input', str(total)


def _flow_discount(rng):
    p = rng.choice([40, 80, 120, 150, 260])
    member = rng.choice(['Y', 'N'])
    price = p
    if p > 100:
        price = price * 0.9
    if member == 'Y':
        price = price - 5
    desc = 'START → INPUT PRICE, MEMBER → decision "PRICE > 100?" – Yes: PRICE ← PRICE × 0.9; then (both paths) decision "MEMBER = \'Y\'?" – Yes: PRICE ← PRICE − 5; then OUTPUT PRICE → END'
    return desc, f'PRICE = {p}, MEMBER = "{member}"', r2(price)


def _flow_halve(rng):
    n0 = n = rng.randint(40, 300)
    c = 0
    while n >= 10:
        n //= 2
        c += 1
    desc = 'START → INPUT N, C ← 0 → decision "N >= 10?" – Yes: N ← N div 2, C ← C + 1, return to the decision; No: OUTPUT N, C → END'
    return desc, f'N = {n0}', f'{n}, {c}'


@R.add('ch08-st2', 'C3', (1, 5), 'short')
def flowchart_out(rng, slot):
    f = rng.choice([_flow_grade, _flow_loop, _flow_discount, _flow_halve])
    desc, inp, out = f(rng)
    return dict(stem=f'A flowchart is described in text below.\n{desc}\nState the output when the input is: {inp}.' if inp != 'no input' else f'A flowchart is described in text below.\n{desc}\nState the output.',
                answer=out, markingKey=f'{out}. 1 mark for following each decision correctly, 1 for the final output.', marks=2 if slot.d <= 3 else 3)


@R.add('ch08-st2', 'C3', (2, 5), 'short')
def pseudo_to_python(rng, slot):
    f = rng.choice(ALGS)
    pseudo, out, cols, rows = f(rng)
    return dict(stem=f'The following algorithm is written in pseudocode.\n{pseudo}\nState the output and describe the purpose of the algorithm.',
                answer=f'Output: {out}. Purpose: it {_ALG_PURPOSE[f.__name__]}.', markingKey=f'Output {out} (2 marks; 1 for a partially correct trace); purpose: {_ALG_PURPOSE[f.__name__]} (1).', marks=3)


K.ar('ch08-st2', [
    ('A diamond is used for decisions in a flowchart.', 'A decision has more than one possible outcome.', 0, 'Both true; R explains why the decision symbol has several exits.'),
    ('Pseudocode must be compiled before it can be tested.', 'Pseudocode is language-independent.', 3, 'A false – pseudocode is not executed; R true.'),
    ('A sentinel-controlled loop is suitable when the number of inputs is unknown.', 'The loop stops when a special value is entered.', 0, 'Both true; R explains A.'),
])


R.facts('ch08-st3', F(
    terms=[('trace table', 'a table that records the value of each variable (and any output) as an algorithm is executed step by step'),
           ('dry run', 'working through an algorithm by hand with test data to check its logic and find errors'),
           ('logic error', 'an error in the design of an algorithm that makes it produce an incorrect result although it runs'),
           ('off-by-one error', 'a logic error in which a loop runs one time too many or too few, often caused by < instead of <='),
           ('test data', 'values chosen to check that an algorithm or program works correctly, including normal, boundary and erroneous data')],
    facts=[('What is the main purpose of a trace table?', 'To follow the values of variables step by step and find logic errors', ['To speed up the program', 'To compile the program', 'To store data permanently'], 'Trace tables support dry runs.'),
           ('A loop "loop I from 0 to N" runs how many times?', 'N + 1', ['N', 'N − 1', '2N'], 'It includes both 0 and N.'),
           ('Which error does a trace table help to find?', 'Logic errors', ['Syntax errors only', 'Hardware faults', 'Network errors'], 'It shows where values diverge from expectations.'),
           ('When completing a trace table, a new row is usually started when…', 'a variable\'s value changes (or a loop iteration starts)', ['the program finishes', 'the user presses Enter', 'a comment is reached'], 'Each row records state at one step.')],
    why=[('Explain why dry running an algorithm with a trace table is useful before writing code.', 'It checks the logic by hand with sample data, revealing errors such as wrong conditions or off-by-one loops early, when they are cheapest to fix, and shows exactly where the algorithm goes wrong.'),
         ('Explain why test data for a loop should include values that make it run zero times.', 'Boundary cases often reveal errors: if the loop body never runs, variables keep their initial values, so wrong initialisation or assumptions about at least one iteration are exposed.'),
         ('Explain why a trace table should include a column for output.', 'It records exactly when and what is output, so it can be compared with the expected output and the step where they diverge can be found.')],
    contrast=[('a dry run', 'testing with a computer', 'A dry run is done by hand, tracing variables on paper to check logic; testing runs the actual program on a computer with test data, which also reveals syntax and run-time errors.'),
              ('a logic error', 'a syntax error', 'A logic error makes the program produce wrong results while it still runs; a syntax error breaks the language rules so the program will not translate or run.')],
    misc=[('A trace table shows only the final values of the variables.', 'A trace table shows how values change at every step, which is what makes it useful for finding logic errors.'),
          ('If an algorithm gives the correct output for one test, it is correct.', 'One test cannot show correctness; normal, boundary and erroneous data must be tested.'),
          ('Off-by-one errors are syntax errors.', 'They are logic errors – the code runs but loops the wrong number of times.')],
    evaluate=[('Trace tables are unnecessary now that programmers have debuggers.', ['debuggers show variables live with breakpoints'], ['trace tables work before any code exists', 'they build understanding of algorithms and are used in exams', 'they help reason about logic, not just observe it'], 'Debuggers complement but do not replace manual tracing, especially in design and learning.')],
    extended=[('A student\'s algorithm should output the average of positive numbers entered until 0 is entered, but outputs the wrong value. Explain how they should use a trace table and appropriate test data to locate and fix the error, giving an example of a likely error.', 'Choose test data (e.g. 4, 6, 0 → 5; 0 only → no division; negatives). Draw columns for each variable, the condition and output; step through, recording changes. Compare with the expected values; e.g. the count is incremented before the sentinel check so 0 is counted, giving 10/3. Fix by checking the sentinel before updating; also guard division by zero.', 6)],
))


@R.add('ch08-st3', 'C3', (2, 5), 'short')
def trace_tab(rng, slot):
    f = rng.choice(ALGS)
    pseudo, out, cols, rows = f(rng)
    if len(rows) > 9 or not rows:
        return None
    tab = table(cols, rows)
    return dict(stem=f'Complete a trace table for the following algorithm, recording the values of {", ".join(cols)} at the end of each iteration, and state the output.\n{pseudo}',
                answer=f'Output {out}. Trace:\n{tab}', markingKey=f'{tab}\nOutput {out}. Award 1 mark per correct pair of rows (max {min(4, (len(rows) + 1) // 2)}), 1 for the output.', marks=min(5, (len(rows) + 1) // 2 + 1))


@R.add('ch08-st3', 'C3', (2, 5), 'short')
def off_by_one(rng, slot):
    n = rng.randint(4, 9)
    arr = [rng.randint(1, 20) for _ in range(n)]
    intended = sum(arr)
    wrong = sum(arr[1:])
    kind = rng.choice(['start1', 'lt'])
    if kind == 'start1':
        pseudo = f'NUMS ← {arr}\nT ← 0\nloop I from 1 to {n - 1}\n    T ← T + NUMS[I]\nend loop\noutput T'
        fix, bad = 'start the loop at 0 (loop I from 0 to ' + str(n - 1) + ')', wrong
    else:
        pseudo = f'NUMS ← {arr}\nT ← 0\nI ← 0\nloop while I < {n - 1}\n    T ← T + NUMS[I]\n    I ← I + 1\nend loop\noutput T'
        fix, bad = f'change the condition to I < {n} (or I <= {n - 1})', sum(arr[:-1])
    return dict(stem=f'This algorithm is meant to output the total of all the values in NUMS (array indices start at 0).\n{pseudo}\nDry run the algorithm, state its actual output, identify the error and correct it.',
                answer=f'Actual output {bad} instead of {intended}; off-by-one error – {fix}', markingKey=f'Actual output {bad} (1); expected {intended} (1); off-by-one error identified (1); correction: {fix} (1).', marks=4)


K.ar('ch08-st3', [
    ('Trace tables help locate logic errors.', 'They show the value of each variable after every step.', 0, 'Both true; R explains A.'),
    ('An off-by-one error stops a program from compiling.', 'Off-by-one errors make a loop run one too many or one too few times.', 3, 'A false – it is a logic error; R true.'),
    ('Boundary test data is chosen at the edges of valid ranges.', 'Many errors occur at the limits of conditions, such as < versus <=.', 0, 'Both true; R explains A.'),
])


R.facts('ch08-st4', F(
    terms=[('heuristic', 'a practical rule of thumb that finds a good-enough solution quickly when an exact solution is too slow to compute'),
           ('greedy algorithm', 'an algorithm that makes the locally best choice at each step, hoping to reach a good overall solution'),
           ('simulation', 'a computer model that imitates the behaviour of a real system over time so that scenarios can be tested'),
           ('optimisation problem', 'a problem in which the best solution must be chosen from many possible solutions according to a measure such as cost or time'),
           ('computational model', 'an abstract, computer-based representation of a real-world system used to make predictions')],
    facts=[('A sat-nav finding the fastest route models roads as…', 'a weighted graph of junctions and roads', ['a binary tree', 'a stack of instructions', 'an unordered list of postcodes'], 'Junctions are nodes; roads are weighted edges.'),
           ('Why do delivery companies often use heuristics to plan routes?', 'Finding the perfect route for many stops takes too long to compute', ['Heuristics always find the best route', 'Computers cannot store maps', 'Routes are random'], 'The travelling-salesman problem grows factorially.'),
           ('A greedy coin-change algorithm repeatedly…', 'chooses the largest coin not exceeding the remaining amount', ['chooses the smallest coin first', 'tries every combination', 'chooses coins at random'], 'It is greedy because it takes the best local choice.'),
           ('Epidemiologists predicting the spread of a virus with a program are using…', 'a simulation (computational model)', ['a compiler', 'a firewall', 'lossless compression'], 'Models allow testing scenarios such as lockdowns.')],
    why=[('Explain why computational thinking helps when designing a timetabling system for a school.', 'Decomposition splits the problem into teachers, rooms, classes and time slots; abstraction keeps only constraints that matter; pattern recognition reuses rules (no clashes, room capacity); an algorithm (constraint search or heuristic) then assigns slots systematically.'),
         ('Explain why simulations are used before building real systems such as new traffic junctions.', 'Changes can be tested safely, cheaply and quickly under many scenarios (peak hours, accidents) before committing money, and the results help choose the best design.'),
         ('Explain why a greedy algorithm does not always give the best solution.', 'It never reconsiders earlier choices; a locally best step can lead to a worse overall result, e.g. coin systems where taking the largest coin first uses more coins.')],
    contrast=[('an exact algorithm', 'a heuristic', 'An exact algorithm guarantees the optimal solution but may be too slow for large problems; a heuristic finds a good solution quickly without a guarantee of optimality.')],
    misc=[('A simulation always predicts exactly what will happen in the real world.', 'A simulation is based on simplified assumptions (abstraction) and input data, so its predictions are approximate and must be validated.'),
          ('Greedy algorithms always give the optimal answer.', 'They are fast but can miss the optimal solution when an early choice prevents a better overall one.'),
          ('Computational thinking only applies when writing code.', 'It is a problem-solving approach used to plan, model and design solutions before or without coding.')],
    evaluate=[('Computer models should be trusted to make decisions about public health policy.', ['can test many scenarios quickly', 'based on data and explicit assumptions'], ['assumptions and data quality may be poor', 'models simplify human behaviour', 'decision-makers must weigh ethical and social factors'], 'Models are valuable decision aids but should inform rather than replace human judgement.')],
    extended=[('A food bank in Glasgow must deliver parcels to 40 households each day with two vans. Apply computational thinking to design a solution, explaining the data that would be needed, the abstraction used and the type of algorithm that would be practical.', 'Decompose: collect addresses/needs, assign households to vans, order stops, print route sheets. Abstraction: graph of addresses (nodes) and travel times (weighted edges); ignore exact street layouts and van details. Pattern: same process every day → reusable program. Algorithm: exact routing is infeasible (TSP), so use a heuristic – cluster by area then nearest-neighbour ordering, possibly improved with 2-opt; check van capacity constraints. Test with real data and refine.', 6)],
))


def _greedy_change(amount, coins):
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c; out.append(c)
    return out


def _opt_change(amount, coins):
    best = [0] + [math.inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return best[amount]


@R.add('ch08-st4', 'C3', (2, 5), 'short')
def coin_change(rng, slot):
    coins = rng.choice([[1, 2, 5, 10, 20, 50], [1, 5, 10, 25], [1, 3, 4], [1, 6, 9], [1, 5, 12], [1, 2, 5, 10]])
    amount = rng.randint(6, 99 if 50 in coins else 30)
    g = _greedy_change(amount, coins)
    o = _opt_change(amount, coins)
    stem = f'A vending machine gives change using the greedy algorithm "repeatedly give the largest coin that does not exceed the amount still owed". The coins available are {", ".join(map(str, coins))}. State the coins given for {amount} and whether this uses the minimum possible number of coins.'
    ans = f'{" + ".join(map(str, g))} ({len(g)} coins); ' + ('this is optimal' if len(g) == o else f'not optimal – {o} coins is possible')
    return dict(stem=stem, answer=ans, markingKey=f'Greedy result {" + ".join(map(str, g))} (2); minimum possible {o} coins (1); conclusion (1).', marks=4)


@R.add('ch08-st4', 'C3', (2, 5), 'short')
def nearest_neighbour(rng, slot):
    pts = {'Depot': (0, 0)}
    for nm in rng.sample(['A', 'B', 'C', 'D', 'E'], 4 if slot.d <= 3 else 5):
        pts[nm] = (rng.randint(-6, 6), rng.randint(-6, 6))
    def dist(a, b):
        return abs(pts[a][0] - pts[b][0]) + abs(pts[a][1] - pts[b][1])
    route, cur, left = ['Depot'], 'Depot', [k for k in pts if k != 'Depot']
    while left:
        nxt = min(left, key=lambda k: (dist(cur, k), k))
        route.append(nxt); left.remove(nxt); cur = nxt
    route.append('Depot')
    tot = sum(dist(a, b) for a, b in zip(route, route[1:]))
    best = min(sum(dist(a, b) for a, b in zip(('Depot',) + p + ('Depot',), p + ('Depot',) + ('Depot',)) if a != b) for p in itertools.permutations([k for k in pts if k != 'Depot']))
    loc = ', '.join(f'{k} {v}' for k, v in pts.items())
    return dict(stem=f'A courier starts and ends at the depot. Locations on a grid (blocks): {loc}. Distance is measured in city blocks (|Δx| + |Δy|). Using the nearest-neighbour heuristic (ties broken alphabetically), give the route and its total distance, and comment on whether a heuristic is appropriate.',
                answer=f'{" → ".join(route)}, {tot} blocks' + (' (optimal here)' if tot == best else f' (the best possible is {best} blocks)'),
                markingKey=f'Route {" → ".join(route)} (2); total {tot} (1); heuristic is fast but not guaranteed optimal – exhaustive search grows factorially (optimum here {best}) (1).', marks=4)


K.ar('ch08-st4', [
    ('Delivery firms use heuristics for route planning.', 'Finding the guaranteed optimal route for many stops is computationally infeasible.', 0, 'Both true; R explains A.'),
    ('A greedy algorithm always reconsiders earlier choices.', 'Greedy algorithms choose the locally best option at each step.', 3, 'A false; R true.'),
    ('Simulations allow scenarios to be tested safely.', 'A simulation models the behaviour of a real system on a computer.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch09 B2.1/B2.3 Programming fundamentals
# =============================================================================================
_FRAMES = ['Consider the following Python code.\n{code}\nState the exact output.',
           'What is printed when this Python program runs?\n{code}',
           'Predict the output of the following code. Show any working needed.\n{code}',
           '{who} writes this Python code:\n{code}\nWrite down exactly what it outputs.']
_VN = [('a', 'b', 'c'), ('x', 'y', 'z'), ('p', 'q', 'r'), ('m', 'n', 'k'), ('num', 'val', 'tmp'), ('width', 'height', 'depth'), ('score', 'bonus', 'total')]


def out_item(rng, code, marks=2, note='', err_ok=False):
    try:
        out = '\n'.join(l.rstrip() for l in run_py(code).split('\n'))
    except Exception as e:
        if not err_ok:
            raise
        out = f'{type(e).__name__} is raised'
    stem = rng.choice(_FRAMES).format(code=code, who=rng.choice(PEOPLE))
    return dict(stem=stem, answer=out.replace('\n', ' / ') if out else '(no output)', type='short', marks=marks,
                markingKey=f'Output (each line separated by /): {out.replace(chr(10), " / ") if out else "(none)"}. {note}'.strip())


R.facts('ch09-st1', F(
    terms=[('variable', 'a named storage location in memory whose value can change while the program runs'),
           ('constant', 'a named value that is set once and does not change while the program runs, e.g. VAT_RATE = 0.2'),
           ('integer', 'a data type for whole numbers, such as −3, 0 or 42'),
           ('float (real)', 'a data type for numbers with a fractional part, stored approximately in floating-point form'),
           ('Boolean', 'a data type with only two values, true and false'),
           ('string', 'a data type for a sequence of characters, such as "Nairobi"'),
           ('casting (type conversion)', 'converting a value from one data type to another, e.g. int("42")'),
           ('assignment', 'giving a variable a value, e.g. total = 0')],
    facts=[('In Python, what is the value of 17 // 5?', '3', ['3.4', '2', '4'], '// is integer (floor) division.'),
           ('In Python, what is the value of 17 % 5?', '2', ['3', '3.4', '0.4'], '% gives the remainder.'),
           ('Which data type is most suitable for storing whether a student has paid a fee?', 'Boolean', ['String', 'Float', 'Integer'], 'Only two states.'),
           ('In Java, what is the result of 7 / 2 when both operands are int?', '3', ['3.5', '4', '3.0'], 'Integer division truncates in Java.'),
           ('Why is a constant used for a value such as the maximum class size?', 'It is defined once, so changing it updates every use and it cannot be changed accidentally', ['It makes the program run in parallel', 'It uses less memory than a variable in all languages', 'It converts the value to a string'], 'Constants improve maintainability and readability.')],
    why=[('Explain why using meaningful variable names and constants improves a program.', 'Names such as totalCost or MAX_SEATS document the purpose of each value, so the code is easier to read, debug and maintain; a constant is changed in one place and protects against accidental modification.'),
         ('Explain why input from the keyboard often needs to be cast before calculations.', 'Input functions return strings; arithmetic on the text "5" would concatenate or cause a type error, so it must be converted with int() or float() first.'),
         ('Explain why floating-point values should not be compared for exact equality.', 'Many decimals (e.g. 0.1) cannot be represented exactly in binary, so small rounding errors occur; 0.1 + 0.2 == 0.3 is false, so a tolerance should be used.')],
    contrast=[('a variable', 'a constant', 'A variable\'s value can change during execution; a constant is assigned once and keeps the same value, documenting a fixed value such as PI.'),
              ('integer division', 'real division', 'Integer division (// in Python, / on two ints in Java) discards the fractional part; real division (/ in Python) gives a floating-point result.')],
    misc=[('In Python, 7 / 2 gives 3 because both numbers are integers.', 'In Python 3, / always gives a float (3.5); // gives integer division (3). (In Java int/int gives 3.)'),
          ('"5" + 3 gives 8 in Python.', 'You cannot add a string and an integer in Python; it raises a TypeError (int("5") + 3 gives 8).'),
          ('A Boolean variable can store the text "yes".', 'A Boolean stores only True or False; "yes" is a string.')],
    evaluate=[('Statically typed languages such as Java are better for beginners than dynamically typed languages such as Python.', ['type errors are caught at compile time', 'explicit types make data clear'], ['more verbose code', 'Python\'s simplicity lets beginners focus on logic', 'dynamic typing allows quick experimentation'], 'Each has merits; static typing helps large programs, dynamic typing lowers the barrier for beginners.')],
    extended=[('A program converts temperatures between Celsius and Fahrenheit for a weather station in Reykjavík. Identify the variables and constants needed, their data types, and explain where casting and rounding are required.', 'Constants: FREEZE = 32 (int), FACTOR = 1.8 (float). Variables: celsius (float), fahrenheit (float), choice (string), valid (Boolean). Casting: input() returns a string, so float(input()); output may use round(f, 1) or formatting; integer division must be avoided. Explain validation (try/except) and naming.', 6)],
))


@R.add('ch09-st1', 'C3', (1, 5), 'short')
def expr_out(rng, slot):
    a, b, c = rng.choice(_VN)
    x, y = rng.randint(7, 60), rng.randint(2, 9)
    forms = [f'{a} = {x}\n{b} = {y}\nprint({a} // {b}, {a} % {b})',
             f'{a} = {x}\n{b} = {y}\nprint({a} / {b})',
             f'{a} = {x}\n{b} = {y}\n{c} = {a} % {b} * 2 + {a} // {b}\nprint({c})',
             f'{a} = "{x}"\n{b} = {y}\nprint({a} * 2, int({a}) + {b})',
             f'{a} = {x}\n{a} = {a} + {y}\n{a} -= {y // 2}\n{a} *= 2\nprint({a})',
             f'{a} = {x}\n{b} = {y}\n{a}, {b} = {b}, {a}\nprint({a} - {b})',
             f'{a} = {x} > {y} and {y} > 5\n{b} = not {a}\nprint({a}, {b}, {a} or {b})',
             f'{a} = {x}.0\nprint(type({a}).__name__, int({a} / {y}), {a} // {y})',
             f'{a} = {x}\n{b} = str({a}) + str({y})\nprint({b}, len({b}))',
             f'{a} = 2 ** {y % 5 + 2} - {x} // {y}\nprint({a})']
    code = rng.choice(forms if slot.d >= 3 else forms[:6])
    return out_item(rng, code, marks=2)


@R.add('ch09-st1', 'C3', (2, 4), 'short')
def type_error_q(rng, slot):
    items = [('age = input("Age: ")   # user types 15\nprint(age + 1)', 'TypeError – input returns a string; use int(input(...))'),
             ('total = 0\nfor p in ["3", "4"]:\n    total = total + p\nprint(total)', 'TypeError – cannot add str to int; use int(p)'),
             ('price = float("12,50")\nprint(price)', 'ValueError – "12,50" is not a valid float literal; use "12.50"'),
             ('count = int("7.5")\nprint(count)', 'ValueError – int() cannot convert the text "7.5"; use int(float("7.5"))'),
             ('rate = 0.1 + 0.2\nif rate == 0.3:\n    print("equal")\nelse:\n    print("not equal")', 'prints not equal – floating-point rounding; compare with abs(rate - 0.3) < 1e-9'),
             ('MAX = 30\nstudents = 31\nif students > MAX:\n    MAX = students\nprint(MAX)', 'prints 31 – Python does not enforce constants; changing MAX defeats its purpose (in Java use final)')]
    code, fix = rng.choice(items)
    try:
        if 'input' in code:
            raise TypeError
        out = run_py(code)
        res = f'Output: {out}'
    except Exception as e:
        res = f'{type(e).__name__}'
    return dict(stem=f'Explain what happens when this code is run and how it should be corrected (if necessary).\n{code}', answer=fix,
                markingKey=f'{res}. {fix}. 1 mark for identifying the behaviour, 1-2 for the explanation/correction.', type='explain', marks=3)


@R.add('ch09-st1', 'C1', (1, 3), 'mcq')
def dtype_mcq(rng, slot):
    vals = [('the number of goals scored in a match', 'integer'), ('a runner\'s 100 m time such as 10.85 s', 'float'), ('whether a door is locked', 'Boolean'),
            ('a passport number such as "K4419920"', 'string'), ('a single grade letter such as \'B\'', 'char (or a one-character string)'), ('a bank balance such as 1520.75', 'float (or decimal)'),
            ('the number of students in a school', 'integer'), ('a telephone number with a leading zero', 'string')]
    what, t = rng.choice(vals)
    return nmcq(rng, f'Which data type is most appropriate for storing {what}?', t, ['integer', 'float', 'Boolean', 'string', 'char (or a one-character string)'], f'{t} best matches the kind of value.')


K.code_tasks('ch09-st1', [
    ('Write a Python function seconds_to_hms(total) that returns a string "H:MM:SS" for a whole number of seconds, e.g. seconds_to_hms(3725) returns "1:02:05".',
     'def seconds_to_hms(total):\n    h = total // 3600\n    m = (total % 3600) // 60\n    s = total % 60\n    return f"{h}:{m:02d}:{s:02d}"',
     'assert seconds_to_hms(3725) == "1:02:05"\nassert seconds_to_hms(59) == "0:00:59"\nassert seconds_to_hms(36000) == "10:00:00"', 4),
    ('Write a Python function bmi(mass_kg, height_m) that returns the body-mass index mass / height² rounded to 1 decimal place, using a constant for the number of decimal places.',
     'DP = 1\ndef bmi(mass_kg, height_m):\n    return round(mass_kg / height_m ** 2, DP)',
     'assert bmi(70, 1.75) == 22.9\nassert bmi(50, 1.6) == 19.5', 3),
], d=(3, 5))


R.facts('ch09-st2', F(
    terms=[('string', 'an ordered, immutable sequence of characters'),
           ('index', 'the position of a character in a string, starting from 0 in Python and Java'),
           ('slicing', 'extracting part of a string using a start and end index, e.g. s[2:5] gives characters 2, 3 and 4'),
           ('concatenation', 'joining two or more strings end to end, e.g. "Data" + "base"'),
           ('immutable', 'unable to be changed after creation; string methods return new strings rather than altering the original'),
           ('substring', 'a contiguous sequence of characters within a string')],
    facts=[('In Python, what is "COMPUTER"[2:5]?', '"MPU"', ['"OMP"', '"MPUT"', '"PUT"'], 'Indices 2, 3, 4.'),
           ('What does len("Hello world") return?', '11', ['10', '12', '2'], 'The space counts as a character.'),
           ('In Python, what is "banana".find("n")?', '2', ['1', '3', '-1'], 'The first n is at index 2.'),
           ('In Java, which method returns the character at a position in a String?', 'charAt()', ['indexOf()', 'substring()', 'length()'], 's.charAt(i) returns the char at index i.')],
    why=[('Explain why s.upper() does not change the string stored in s in Python.', 'Strings are immutable; upper() returns a new upper-case string, so the result must be assigned (s = s.upper()) to keep it.'),
         ('Explain why string comparison "apple" < "banana" is true but "Zebra" < "apple" is also true.', 'Strings are compared character by character using their character codes; upper-case letters (65-90) have lower codes than lower-case (97-122), so "Z" < "a".'),
         ('Explain why indexing a string outside its length causes an error.', 'Valid indices run from 0 to len − 1; accessing beyond this refers to memory that is not part of the string, so Python raises IndexError (Java StringIndexOutOfBoundsException) instead of returning garbage.')],
    contrast=[('s.find(x)', 's.index(x)', 'Both return the first position of x; find returns −1 if x is not found, while index raises a ValueError.'),
              ('indexing', 'slicing', 'Indexing returns a single character at one position (s[3]); slicing returns a substring between two positions (s[1:4]).')],
    misc=[('In Python, s[1:4] includes the character at index 4.', 'The end index is exclusive: s[1:4] gives indices 1, 2 and 3.'),
          ('The first character of a string is at index 1.', 'In Python and Java the first index is 0.'),
          ('s.replace("a", "o") changes s directly.', 'It returns a new string; s is unchanged unless reassigned.')],
    evaluate=[('Strings should always be compared in a case-insensitive way.', ['users type names inconsistently', 'avoids duplicate accounts like "Ana" and "ana"'], ['passwords and codes must be case-sensitive', 'some languages have complex case rules'], 'Depends on context: case-insensitive for names and searches, case-sensitive for passwords and identifiers.')],
    extended=[('A school generates usernames from a student\'s first name, surname and year of entry, e.g. ("Amara", "Okafor", 2026) → "okafam26". Design the algorithm using string methods, explain how it handles names shorter than four letters, and how duplicates could be avoided.', 'username = (surname[:4] + first[:2]).lower() + str(year)[-2:]; slicing returns the whole string if it is shorter, so "Li" gives "li"; remove spaces/hyphens with replace; check existing usernames in a set and append a counter (okafam26, okafam26b/2) if taken.', 6)],
))


@R.add('ch09-st2', 'C3', (1, 5), 'short')
def str_out(rng, slot):
    w = rng.choice(['ALGORITHM', 'Singapore', 'Database', 'Recursion', 'Bandwidth', 'Encryption', 'Variable', 'Kilimanjaro', 'Montevideo'])
    n = len(w)
    i, j = sorted(rng.sample(range(n), 2))
    v = rng.choice(['s', 'word', 'city', 'txt', 'msg'])
    forms = [f'{v} = "{w}"\nprint({v}[{i}], {v}[{i}:{j}], {v}[-1])',
             f'{v} = "{w}"\nprint(len({v}), {v}.upper()[:{j}], {v}.lower().count("{w[i].lower()}"))',
             f'{v} = "{w}"\nprint({v}[::-1][:{j - i + 1}])',
             f'{v} = "{w}"\nprint({v}.find("{w[j]}"), {v}.replace("{w[i]}", "*"))',
             f'{v} = "{w}"\nout = ""\nfor ch in {v}:\n    if ch.lower() in "aeiou":\n        out = out + ch\nprint(out, len(out))',
             f'{v} = "{w}"\nprint({v}[{i}:] + {v}[:{i}])',
             f'{v} = "{w} is {n} letters"\nparts = {v}.split()\nprint(len(parts), parts[0][{i % 4}], parts[-1].title())',
             f'{v} = "{w}"\nres = ""\nfor k in range(0, len({v}), {rng.randint(2, 3)}):\n    res += {v}[k]\nprint(res)']
    code = rng.choice(forms if slot.d >= 3 else forms[:4])
    return out_item(rng, code, marks=2 if slot.d <= 3 else 3)


@R.add('ch09-st2', 'C3', (2, 5), 'short')
def str_java(rng, slot):
    w = rng.choice(['NETWORK', 'Python', 'Ethernet', 'Compiler', 'Quantum'])
    i, j = sorted(rng.sample(range(len(w)), 2))
    out = f'{len(w)} {w[i]} {w[i:j]} {w.find(w[j])}'
    code = f'String s = "{w}";\nSystem.out.println(s.length() + " " + s.charAt({i}) + " " + s.substring({i}, {j}) + " " + s.indexOf("{w[j]}"));'
    return dict(stem=f'State the output of this Java statement.\n{code}', answer=out,
                markingKey=f'{out}: length {len(w)}; charAt({i}) = {w[i]}; substring({i}, {j}) = "{w[i:j]}" (end exclusive); indexOf gives the first occurrence {w.find(w[j])}. 1 mark per two correct parts.', marks=2)


K.ar('ch09-st2', [
    ('Python strings are immutable.', 'String methods such as upper() return a new string.', 0, 'Both true; R is a consequence that illustrates A.'),
    ('"Data"[4] returns the last character.', 'Python indexing starts at 0.', 3, 'A false – index 4 is out of range (IndexError); R true.'),
    ('"Zoo" < "apple" is True in Python.', 'Upper-case letters have smaller character codes than lower-case letters.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch09-st2', [
    ('Write a Python function is_palindrome(text) that returns True if text reads the same forwards and backwards, ignoring case and spaces.',
     'def is_palindrome(text):\n    t = text.replace(" ", "").lower()\n    return t == t[::-1]',
     'assert is_palindrome("Never odd or even")\nassert not is_palindrome("Lima")\nassert is_palindrome("a")', 4),
    ('Write a Python function count_vowels(s) that returns the number of vowels (a, e, i, o, u, either case) in s, using a loop.',
     'def count_vowels(s):\n    n = 0\n    for ch in s.lower():\n        if ch in "aeiou":\n            n += 1\n    return n',
     'assert count_vowels("Kuala Lumpur") == 5\nassert count_vowels("rhythm") == 0', 3),
    ('Write a Python function initials(full_name) that returns the upper-case initials of each word, e.g. initials("ada king lovelace") returns "AKL".',
     'def initials(full_name):\n    return "".join(w[0].upper() for w in full_name.split())',
     'assert initials("ada king lovelace") == "AKL"\nassert initials("Grace Hopper") == "GH"', 3),
], d=(3, 5))


R.facts('ch09-st3', F(
    terms=[('selection', 'a construct (if, elif/else if, else, switch) that chooses which statements to execute depending on a condition'),
           ('count-controlled loop', 'a loop that repeats a fixed number of times, such as a for loop over a range'),
           ('condition-controlled loop', 'a loop that repeats while (or until) a condition is true, such as a while loop'),
           ('nested loop', 'a loop placed inside another loop, so the inner loop runs fully for each iteration of the outer loop'),
           ('infinite loop', 'a loop whose terminating condition is never met, so it never ends'),
           ('Boolean operator', 'an operator (and, or, not) that combines or inverts conditions')],
    facts=[('How many times does print run in: for i in range(3, 12, 3): print(i)?', '3', ['4', '9', '12'], 'i takes 3, 6, 9.'),
           ('Which loop is best when the number of repetitions is unknown in advance?', 'A while loop', ['A for loop over a fixed range', 'A nested for loop', 'An if statement'], 'It repeats until a condition changes.'),
           ('In Java, which loop always executes its body at least once?', 'do-while', ['while', 'for', 'for-each'], 'The condition is tested after the body.'),
           ('What does break do inside a loop?', 'Exits the loop immediately', ['Skips to the next iteration', 'Restarts the loop', 'Ends the whole program'], 'continue skips; break exits.')],
    why=[('Explain why the order of conditions matters in an if-elif-else chain that assigns grades.', 'Conditions are checked from the top and the first true branch runs; if score >= 50 were tested before score >= 80, an 85 would be given the lower grade, so the most restrictive condition must come first.'),
         ('Explain why a while loop may cause an infinite loop but a for loop over range() normally cannot.', 'A while loop ends only when its condition becomes false, which depends on the body changing variables; if they never change it runs forever. A for loop over a range runs a fixed number of times determined in advance.'),
         ('Explain how a nested loop can be used to print a multiplication table.', 'The outer loop iterates over rows (first factor) and, for each row, the inner loop iterates over columns (second factor), printing their product; the inner loop restarts for every outer iteration.')],
    contrast=[('a while loop', 'a for loop', 'A while loop is condition-controlled and repeats while a condition holds (unknown number of times); a for loop is count-controlled or iterates over a collection a known number of times.'),
              ('break', 'continue', 'break exits the loop completely; continue skips the rest of the current iteration and moves to the next one.')],
    misc=[('range(1, 5) produces the numbers 1 to 5.', 'The end value is excluded: range(1, 5) produces 1, 2, 3, 4.'),
          ('An else block after if runs every time.', 'else runs only when the if condition (and any elif conditions) are false.'),
          ('A nested loop with an outer loop of 4 and an inner loop of 5 iterations runs the inner body 9 times.', 'The inner body runs 4 × 5 = 20 times.')],
    evaluate=[('Programs should avoid nested loops wherever possible.', ['nested loops can be O(n²) and slow on big data', 'deep nesting is hard to read'], ['many problems (2D grids, comparing pairs) need them', 'clear nested loops are better than obscure alternatives'], 'Avoid unnecessary nesting for efficiency and readability, but nested loops are the correct tool for many problems.')],
    extended=[('A cinema in Kraków charges 25 zł for adults, 15 zł for children under 12 and 18 zł for seniors (65+), with 20% off all tickets on Tuesdays. Write a Python program that reads ages until 0 is entered, then outputs the number of tickets of each type and the total cost for a given day.', 'Model answer uses: day = input(); counts for adult/child/senior; while True: age = int(input()); if age == 0: break; if age < 12 … elif age >= 65 … else …; total += price; if day == "Tuesday": total *= 0.8; print results. Marks: loop with sentinel, correct selection order and boundaries, discount, output.', 6)],
))


@R.add('ch09-st3', 'C3', (1, 5), 'short')
def loop_out(rng, slot):
    a, b, c = rng.choice(_VN)
    s, e, st = rng.randint(0, 4), rng.randint(8, 16), rng.randint(1, 3)
    k = rng.randint(2, 5)
    forms = [f'{c} = 0\nfor {a} in range({s}, {e}, {st}):\n    {c} = {c} + {a}\nprint({c})',
             f'{a} = {e * 3}\n{b} = 0\nwhile {a} > {k}:\n    {a} = {a} // 2\n    {b} += 1\nprint({a}, {b})',
             f'for {a} in range(1, {k + 1}):\n    print({a} * {st}, end=" ")\nprint()',
             f'{c} = 0\nfor {a} in range({k}):\n    for {b} in range({a}, {k}):\n        {c} += 1\nprint({c})',
             f'{b} = []\nfor {a} in range({s}, {e}):\n    if {a} % {k} == 0:\n        continue\n    if {a} > {e - 3}:\n        break\n    {b}.append({a})\nprint({b})',
             f'{a} = {e}\n{b} = 1\nwhile {a} != 1:\n    if {a} % 2 == 0:\n        {a} = {a} // 2\n    else:\n        {a} = {a} + 1\n    {b} += 1\nprint({b})',
             f'{a} = {rng.randint(30, 99)}\nif {a} >= 80:\n    print("A")\nelif {a} >= 60:\n    print("B")\nelif {a} % 2 == 0:\n    print("C")\nelse:\n    print("D")',
             f'{c} = ""\nfor {a} in range({k}):\n    {c} = {c} + "*" * ({a} + 1) + "|"\nprint({c})']
    code = rng.choice(forms if slot.d >= 3 else [forms[0], forms[2], forms[6], forms[7]])
    return out_item(rng, code, marks=2 if slot.d <= 3 else 3)


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def loop_count(rng, slot):
    n, m = rng.randint(3, 9), rng.randint(2, 7)
    kind = rng.choice(['nested', 'tri', 'while'])
    if kind == 'nested':
        code = f'for i in range({n}):\n    for j in range({m}):\n        print(i, j)'
        cnt = n * m
    elif kind == 'tri':
        code = f'for i in range({n}):\n    for j in range(i):\n        print(i, j)'
        cnt = n * (n - 1) // 2
    else:
        x = rng.randint(50, 500)
        code = f'x = {x}\nwhile x > 1:\n    print(x)\n    x = x // {m}'
        cnt, y = 0, x
        while y > 1:
            cnt += 1; y //= m
    return dict(stem=f'How many times is print executed when this code runs? Show your reasoning.\n{code}', answer=str(cnt),
                markingKey=f'{cnt} (A1) with reasoning (M1), e.g. ' + ({'nested': f'{n} × {m}', 'tri': f'0 + 1 + … + {n - 1} = {n}×{n - 1}/2'}.get(kind, f'repeated integer division by {m}')) + '.', marks=2)


K.ar('ch09-st3', [
    ('range(5) produces five values.', 'Python lists are indexed from 0.', 1, 'Both true, but list indexing is not the reason range(5) yields 0-4; range simply counts from 0 up to (not including) 5.'),
    ('A do-while loop in Java always runs at least once.', 'The condition is checked after the loop body.', 0, 'Both true; R explains A.'),
    ('The else branch of an if statement runs when the condition is true.', 'if-else chooses between two paths.', 3, 'A false; R true.'),
])

K.code_tasks('ch09-st3', [
    ('Write a Python function fizzbuzz(n) that returns a list of strings for 1..n where multiples of 3 are "Fizz", multiples of 5 "Buzz", multiples of both "FizzBuzz" and other numbers their digits.',
     'def fizzbuzz(n):\n    out = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            out.append("FizzBuzz")\n        elif i % 3 == 0:\n            out.append("Fizz")\n        elif i % 5 == 0:\n            out.append("Buzz")\n        else:\n            out.append(str(i))\n    return out',
     'assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]\nassert fizzbuzz(15)[-1] == "FizzBuzz"', 4),
    ('Write a Python function is_prime(n) that returns True if the integer n is prime, using a loop that tests divisors only up to the square root of n.',
     'def is_prime(n):\n    if n < 2:\n        return False\n    d = 2\n    while d * d <= n:\n        if n % d == 0:\n            return False\n        d += 1\n    return True',
     'assert [x for x in range(20) if is_prime(x)] == [2, 3, 5, 7, 11, 13, 17, 19]', 4),
    ('Write a Python function grade(score) that returns "7" for 85 and above, "6" for 70-84, "5" for 55-69, "4" for 40-54 and "Fail" below 40; it should return "Invalid" for scores outside 0-100.',
     'def grade(score):\n    if score < 0 or score > 100:\n        return "Invalid"\n    if score >= 85:\n        return "7"\n    elif score >= 70:\n        return "6"\n    elif score >= 55:\n        return "5"\n    elif score >= 40:\n        return "4"\n    return "Fail"',
     'assert grade(85) == "7" and grade(84) == "6" and grade(40) == "4" and grade(39) == "Fail" and grade(101) == "Invalid"', 4),
], d=(3, 5))


R.facts('ch09-st4', F(
    terms=[('function', 'a named, reusable block of code that performs a task and may take parameters and return a value'),
           ('parameter', 'a variable listed in a function definition that receives a value when the function is called'),
           ('argument', 'the actual value passed to a function when it is called'),
           ('return value', 'the value a function sends back to the code that called it'),
           ('local variable', 'a variable declared inside a function, accessible only within that function while it runs'),
           ('global variable', 'a variable declared outside all functions, accessible throughout the program'),
           ('scope', 'the region of a program in which a variable can be accessed'),
           ('procedure', 'a subroutine that performs a task but does not return a value (a void method in Java)')],
    facts=[('What does a Python function return if it has no return statement?', 'None', ['0', 'An empty string', 'The last value computed'], 'Python functions return None by default.'),
           ('In def area(w, h):, w and h are…', 'parameters', ['arguments', 'global variables', 'return values'], 'Arguments are the values passed at the call.'),
           ('Which keyword lets a Python function assign to a global variable?', 'global', ['static', 'public', 'return'], 'Without it, assignment creates a local variable.'),
           ('In Java, a method that does not return a value is declared with return type…', 'void', ['null', 'empty', 'static'], 'void means no return value.')],
    why=[('Explain why programs are divided into functions.', 'Functions can be written and tested independently (decomposition), reused with different arguments instead of duplicating code, make programs easier to read and maintain, and allow teams to work on different parts.'),
         ('Explain why local variables are preferred to global variables.', 'Local variables exist only inside their function, so they cannot be changed accidentally elsewhere, names can be reused safely, functions are self-contained and easier to test, and memory is freed when the function ends.'),
         ('Explain why a function that modifies a list parameter can change the caller\'s list.', 'In Python (and for object references in Java) the parameter refers to the same list object as the argument, so mutating it (e.g. append) changes the original; reassigning the parameter would not.')],
    contrast=[('a parameter', 'an argument', 'A parameter is the variable named in the function definition; an argument is the value supplied in a particular call.'),
              ('a local variable', 'a global variable', 'A local variable is created inside a function and only exists there while it runs; a global variable is defined outside functions and accessible throughout the program.'),
              ('a function', 'a procedure', 'A function returns a value to the caller; a procedure performs actions but returns no value.')],
    misc=[('Changing a parameter that holds an integer inside a function changes the caller\'s variable.', 'Integers are immutable; rebinding the parameter only affects the local name, so the caller\'s variable is unchanged.'),
          ('A function can only be called once.', 'Functions can be called any number of times, with different arguments.'),
          ('print and return do the same thing.', 'print displays a value to the user; return sends a value back to the calling code for further use.')],
    evaluate=[('Global variables make programs simpler and should be used freely.', ['avoid passing many parameters', 'easy access for small scripts'], ['any function can change them, causing hard-to-find bugs', 'functions become dependent and hard to test or reuse', 'name clashes'], 'Use sparingly (e.g. constants); prefer parameters and return values.')],
    extended=[('Design a modular Python program for a library in Accra that calculates late fees: 0.50 cedi per day for the first 7 days late and 1 cedi per day after, capped at 20 cedi. Define the functions you would use, their parameters and return values, and explain how scope keeps them independent.', 'days_late(due, returned) → int; late_fee(days) → float: if days <= 7: fee = 0.5*days else fee = 3.5 + (days − 7); return min(fee, 20); format_receipt(name, fee) → str; main() reads data and calls them. Each function uses local variables and communicates only through parameters/returns, so it can be tested independently (e.g. late_fee(10) = 6.5).', 6)],
))


@R.add('ch09-st4', 'C3', (2, 5), 'short')
def func_out(rng, slot):
    a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(1, 5)
    fn = rng.choice(['calc', 'f', 'update', 'change', 'process', 'mystery'])
    forms = [f'def {fn}(x, y):\n    return x * y - {c}\n\nprint({fn}({a}, {b}) + {fn}({b}, 1))',
             f'n = {a}\ndef {fn}(n):\n    n = n + {b}\n    return n\n\nprint({fn}(n), n)',
             f'total = {a}\ndef {fn}():\n    global total\n    total = total * {b}\n\n{fn}()\n{fn}()\nprint(total)',
             f'def {fn}(lst):\n    lst.append({a})\n    lst = [{b}]\n    return lst\n\nnums = [{c}]\nres = {fn}(nums)\nprint(nums, res)',
             f'def {fn}(x, y={b}):\n    return x // y, x % y\n\nq, r = {fn}({a * b + c})\nprint(q, r, {fn}({a * 10}, {a})[0])',
             f'def {fn}(s):\n    if len(s) <= 1:\n        return s\n    return {fn}(s[1:]) + s[0]\n\nprint({fn}("{rng.choice(["LOOP", "STACK", "ARRAY", "QUEUE"])}"))',
             f'x = {a}\ndef {fn}(y):\n    x = y * 2\n    return x + {c}\n\nz = {fn}(x)\nprint(x, z)',
             f'def {fn}(n):\n    if n == 0:\n        print("done")\n        return\n    print(n)\n    {fn}(n - {1 if a > 4 else 2 if a % 2 == 0 else 1})\n\n{fn}({a if a % 2 == 0 or a > 4 else a + 1})']
    code = rng.choice(forms)
    return out_item(rng, code, marks=2 if slot.d <= 3 else 3, note='Award marks only for the exact values; scope and mutability must be applied correctly.')


@R.add('ch09-st4', 'C3', (2, 4), 'short')
def scope_id(rng, slot):
    code = rng.choice([
        ('rate = 0.15\ndef tax(price):\n    amount = price * rate\n    return amount\n\nprint(tax(200))\nprint(amount)', 'rate – global; price – parameter (local); amount – local. The last line raises NameError because amount only exists inside tax.'),
        ('count = 0\ndef add_one():\n    count = count + 1\n\nadd_one()\nprint(count)', 'count is global but assigned inside add_one without "global", so Python treats it as local and raises UnboundLocalError; fix with "global count" or by returning a value.'),
        ('def double(nums):\n    for i in range(len(nums)):\n        nums[i] *= 2\n\nvals = [1, 2, 3]\ndouble(vals)\nprint(vals)', 'nums is a parameter that refers to the same list as vals, so the caller\'s list is changed: output [2, 4, 6]; i is local.'),
    ])
    src, ans = code
    try:
        out = run_py(src)
        res = f'Output {out.replace(chr(10), " / ")}'
    except Exception as e:
        res = f'{type(e).__name__} raised'
    return dict(stem=f'Identify the scope of each variable in the code below and explain what happens when it runs.\n{src}', answer=ans,
                markingKey=f'{res}. {ans} 1 mark per correctly classified variable (max 2), 1-2 marks for the explanation.', type='explain', marks=4)


K.ar('ch09-st4', [
    ('A local variable cannot be accessed outside its function.', 'Local variables exist only while their function is running.', 0, 'Both true; R explains A.'),
    ('A function with no return statement returns 0 in Python.', 'Every Python function returns a value.', 3, 'A false (it returns None); R true.'),
    ('Passing a list to a function lets the function modify the original list.', 'The parameter refers to the same list object as the argument.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch09-st4', [
    ('Write a Python function late_fee(days) that returns 0.5 per day for the first 7 days late and 1.0 per day after that, capped at 20. Then write a function total_fees(list_of_days) that uses late_fee to return the total for many loans.',
     'def late_fee(days):\n    if days <= 0:\n        return 0\n    fee = 0.5 * min(days, 7) + 1.0 * max(0, days - 7)\n    return min(fee, 20)\n\ndef total_fees(list_of_days):\n    return sum(late_fee(d) for d in list_of_days)',
     'assert late_fee(3) == 1.5\nassert late_fee(10) == 6.5\nassert late_fee(40) == 20\nassert total_fees([0, 3, 10]) == 8.0', 5),
    ('Write a Python function stats(values) that returns a tuple (minimum, maximum, mean rounded to 2 dp) without using the built-in min, max or sum.',
     'def stats(values):\n    lo = hi = values[0]\n    total = 0\n    for v in values:\n        if v < lo:\n            lo = v\n        if v > hi:\n            hi = v\n        total += v\n    return lo, hi, round(total / len(values), 2)',
     'assert stats([4, 8, 1, 7]) == (1, 8, 5.0)\nassert stats([2]) == (2, 2, 2.0)', 5),
], d=(3, 5))


R.facts('ch09-st5', F(
    terms=[('exception', 'an error event that occurs during execution and disrupts the normal flow of the program, such as division by zero'),
           ('exception handling', 'using constructs such as try/except (Python) or try/catch (Java) to detect run-time errors and respond without crashing'),
           ('syntax error', 'an error in which code breaks the grammar rules of the language, so it cannot be translated'),
           ('run-time error', 'an error that occurs while the program is running, such as dividing by zero or opening a missing file'),
           ('logic error', 'an error in which the program runs but produces incorrect results because the algorithm is wrong'),
           ('boundary data', 'test data at the edges of the valid range, together with the values just outside it'),
           ('erroneous data', 'test data that should be rejected by the program, such as text where a number is expected'),
           ('debugging', 'the process of finding and fixing errors in a program, e.g. with print statements, breakpoints and trace tables')],
    facts=[('Which test data is boundary data for an age field accepting 13 to 19 inclusive?', '13 and 19 (and 12 and 20 just outside)', ['16', '"thirteen"', '-5'], 'Boundaries are the limits of the valid range.'),
           ('Dividing by zero in Python raises…', 'ZeroDivisionError', ['ValueError', 'SyntaxError', 'IndexError'], 'It is a run-time error.'),
           ('In a try/except/finally structure, when does the finally block run?', 'Always, whether or not an exception occurred', ['Only if no exception occurred', 'Only if an exception occurred', 'Never'], 'finally is used for clean-up.'),
           ('A program to compute averages prints 7 instead of 7.5. This is most likely a…', 'logic error', ['syntax error', 'run-time error', 'compilation error'], 'The program runs but the result is wrong (e.g. integer division).')],
    why=[('Explain why exception handling makes programs more robust.', 'Unexpected events such as invalid input, missing files or lost connections are caught and dealt with (error message, retry, default value) instead of crashing the program and losing the user\'s work.'),
         ('Explain why a test plan includes normal, boundary and erroneous data.', 'Normal data checks typical operation, boundary data checks the edges where off-by-one errors occur, and erroneous data checks that invalid input is rejected; together they give confidence that the program handles all cases.'),
         ('Explain why logic errors are often harder to find than syntax errors.', 'The translator reports syntax errors with line numbers, but logic errors produce no error message; the programmer must notice wrong output and trace the code to find where the algorithm is incorrect.')],
    contrast=[('a syntax error', 'a run-time error', 'A syntax error breaks language rules and is found before execution; a run-time error occurs while the program runs, e.g. division by zero, even though the syntax is valid.'),
              ('validation', 'exception handling', 'Validation checks input against rules before it is used (range, type, format); exception handling catches errors that occur during execution and responds to them.')],
    misc=[('A program that runs without crashing has no errors.', 'It may still contain logic errors that give wrong results.'),
          ('Boundary testing means testing only the largest possible value.', 'Boundary testing uses values at both ends of the range and just outside them.'),
          ('Catching every exception with a bare except is good practice.', 'A bare except hides unexpected bugs; catch specific exceptions and handle each appropriately.')],
    evaluate=[('Thorough testing can prove that a program has no errors.', ['systematic tests find most errors', 'boundary and erroneous data cover risky cases'], ['it is impossible to test every input', 'testing shows the presence of errors, not their absence', 'formal verification is needed for proof'], 'Testing increases confidence but cannot prove correctness except for trivially small input spaces.')],
    extended=[('A ticket-booking program asks for the number of tickets (1-10). Write a Python function get_tickets() that keeps asking until a valid integer in range is entered, using exception handling, and design a test table with normal, boundary and erroneous data and expected results.', 'def get_tickets(): while True: try: n = int(input("Tickets: ")) except ValueError: print("Enter a whole number"); continue; if 1 <= n <= 10: return n; print("Must be 1-10"). Test table: 5 normal → accepted; 1, 10 boundary valid → accepted; 0, 11 boundary invalid → rejected; "three", 2.5, blank erroneous → rejected with message.', 6)],
))


@R.add('ch09-st5', 'C3', (2, 5), 'short')
def try_out(rng, slot):
    a = rng.randint(1, 9)
    vals = rng.sample(['0', '5', '"x"', '2', '-1', '10'], 4)
    forms = [f'data = [{", ".join(vals)}]\nfor v in data:\n    try:\n        print({a * 10} // int(v))\n    except ZeroDivisionError:\n        print("div0")\n    except ValueError:\n        print("bad")\n    except TypeError:\n        print("type")',
             f'def safe(v):\n    try:\n        r = {a * 12} / v\n    except ZeroDivisionError:\n        return -1\n    else:\n        return round(r, 1)\n    finally:\n        print("checked", v)\n\nprint(safe({rng.choice([0, 3, 4, 5])}))',
             f'items = [{a}, {a + 1}, {a + 2}]\ntry:\n    print(items[{rng.randint(1, 4)}])\n    print("ok")\nexcept IndexError:\n    print("no such item")\nfinally:\n    print("end")',
             f'total = 0\nfor s in ["{a}", "{a}.5", "seven", "{a + 3}"]:\n    try:\n        total += int(s)\n    except ValueError:\n        total -= 1\nprint(total)']
    code = rng.choice(forms)
    code = code.replace('"x"', '"x"')
    return out_item(rng, code, marks=3, note='Exceptions raised inside try are caught by the matching except; finally always runs.')


@R.add('ch09-st5', 'C3', (1, 4), 'short')
def test_data(rng, slot):
    lo, hi = rng.choice([(1, 10), (13, 19), (0, 100), (18, 65), (5, 30), (1, 31)])
    field = rng.choice(['number of tickets', 'student age', 'exam percentage', 'applicant age', 'quantity ordered', 'day of the month'])
    normal = rng.randint(lo + 1, hi - 1)
    return dict(stem=f'A program accepts a {field} that must be an integer from {lo} to {hi} inclusive. Give one example each of normal, boundary and erroneous test data, with the expected outcome for each.',
                answer=f'Normal: {normal} – accepted; boundary: {lo} and {hi} accepted, {lo - 1} and {hi + 1} rejected; erroneous: "abc" or {hi + rng.randint(20, 90)} or 4.5 – rejected with an error message',
                markingKey=f'Normal e.g. {normal} accepted (1); boundary {lo}/{hi} accepted and/or {lo - 1}/{hi + 1} rejected (1); erroneous e.g. text, decimals or far out of range rejected (1).', marks=3)


@R.add('ch09-st5', 'C3', (2, 5), 'short')
def error_type(rng, slot):
    items = [('average = total / count   # count is 0 when no marks are entered', 'run-time error (ZeroDivisionError)', 'check count > 0 before dividing or handle the exception'),
             ('if score > 50\n    print("pass")', 'syntax error (missing colon)', 'add a colon after the condition'),
             ('area = length + width   # should calculate the area of a rectangle', 'logic error', 'use length * width'),
             ('for i in range(1, 10):   # intended to print 1 to 10\n    print(i)', 'logic error (off-by-one)', 'use range(1, 11)'),
             ('names = ["Ana", "Ben"]\nprint(names[2])', 'run-time error (IndexError)', 'valid indices are 0 and 1; use names[1] or check len(names)'),
             ('print("Total: " + 5)', 'run-time error (TypeError)', 'convert with str(5) or use an f-string'),
             ('while x > 0:\n    print(x)   # x is never changed', 'logic error (infinite loop)', 'update x inside the loop, e.g. x -= 1'),
             ('Pront("hello")', 'run-time error (NameError) – misspelt identifier', 'correct to print'),
             ('celsius = (fahrenheit - 32) * 9 / 5', 'logic error', 'the factor should be 5 / 9')]
    picks = rng.sample(items, 2 if slot.d <= 3 else 3)
    ans = '; '.join(f'({chr(97 + i)}) {t} – fix: {f}' for i, (c, t, f) in enumerate(picks))
    return dict(stem='For each code fragment, identify the type of error (syntax, run-time or logic) and suggest a correction.\n' + '\n'.join(f'({chr(97 + i)})\n{c}' for i, (c, t, f) in enumerate(picks)),
                answer=ans, markingKey=f'1 mark for each error type, 1 for each correction: {ans}.', type='explain', marks=2 * len(picks))


K.ar('ch09-st5', [
    ('A finally block runs even if an exception is raised.', 'finally is used to release resources such as open files.', 1, 'Both true, but R gives a use of finally rather than the reason it always runs.'),
    ('Syntax errors are detected before a compiled program runs.', 'The compiler checks the code against the grammar of the language.', 0, 'Both true; R explains A.'),
    ('A program that passes all tests is free of errors.', 'Testing uses normal, boundary and erroneous data.', 3, 'A false – testing cannot prove the absence of errors; R true.'),
])

K.code_tasks('ch09-st5', [
    ('Write a Python function parse_ages(texts) that takes a list of strings and returns a list of the valid integer ages from 0 to 120, skipping any string that cannot be converted, using exception handling.',
     'def parse_ages(texts):\n    ages = []\n    for t in texts:\n        try:\n            a = int(t)\n        except ValueError:\n            continue\n        if 0 <= a <= 120:\n            ages.append(a)\n    return ages',
     'assert parse_ages(["17", "x", "130", "0", "4.5", "120"]) == [17, 0, 120]', 4),
    ('Write a Python function safe_divide(a, b) that returns a / b rounded to 2 dp, or the string "undefined" if b is zero, and "invalid" if either value is not a number, using try/except.',
     'def safe_divide(a, b):\n    try:\n        return round(a / b, 2)\n    except ZeroDivisionError:\n        return "undefined"\n    except TypeError:\n        return "invalid"',
     'assert safe_divide(7, 2) == 3.5\nassert safe_divide(1, 0) == "undefined"\nassert safe_divide("1", 2) == "invalid"', 4),
], d=(3, 5))


# =============================================================================================
# ch10 B2.2 Data structures
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('array', 'a data structure that stores a fixed number of elements of the same data type in contiguous memory, accessed by index'),
           ('list (dynamic array)', 'an ordered collection that can grow and shrink at run time, such as a Python list or Java ArrayList'),
           ('two-dimensional array', 'an array of arrays, used to represent data in rows and columns, accessed with two indices'),
           ('index', 'the integer position of an element in an array or list, starting from 0'),
           ('static data structure', 'a structure whose size is fixed when it is created, such as a Java array'),
           ('dynamic data structure', 'a structure whose size can change during execution, such as a list')],
    facts=[('In Python, what is the index of the last element of a list nums?', 'len(nums) - 1', ['len(nums)', '-0', '1'], 'Indices start at 0 (or use -1).'),
           ('A 2D array grid has 4 rows and 6 columns. How many elements does it hold?', '24', ['10', '6', '4'], 'rows × columns.'),
           ('In Java, int[] a = new int[5]; what is the initial value of a[2]?', '0', ['null', 'undefined', '5'], 'Numeric arrays are initialised to 0.'),
           ('Which operation is fastest on an array?', 'Accessing an element by its index', ['Inserting at the front', 'Searching an unsorted array for a value', 'Deleting from the middle'], 'Index access is O(1).')],
    why=[('Explain why accessing an array element by index is very fast.', 'Elements are stored contiguously and have the same size, so the address of element i is base + i × size, which is computed directly in constant time without searching.'),
         ('Explain why inserting an item at the start of a list of n elements is slow.', 'Every existing element must be shifted one position to the right to make room, which takes time proportional to n (O(n)).'),
         ('Explain why a 2D array is suitable for storing a seating plan or a game board.', 'The data has a natural row-and-column structure; grid[r][c] gives direct access to any cell and nested loops can process rows and columns systematically.')],
    contrast=[('a static array', 'a dynamic list', 'A static array has a fixed size set at creation (Java int[]) and all elements of one type; a dynamic list (ArrayList, Python list) can grow or shrink as items are added or removed.'),
              ('a 1D array', 'a 2D array', 'A 1D array is a single row of elements accessed with one index; a 2D array is a table of rows and columns accessed with two indices.')],
    misc=[('In Python, nums[len(nums)] returns the last element.', 'Valid indices go up to len(nums) − 1; nums[len(nums)] raises IndexError.'),
          ('A Java array can grow automatically when it is full.', 'Java arrays have a fixed size; an ArrayList (or creating a new larger array) is needed.'),
          ('grid[2][3] means column 2, row 3.', 'By convention grid[2][3] is row 2, column 3 (the first index selects the row).')],
    evaluate=[('Lists are always better than arrays.', ['flexible size and convenient methods'], ['arrays use less memory and give predictable performance', 'fixed-size data (e.g. 12 months) suits arrays', 'some languages and embedded systems only provide arrays'], 'Lists are convenient for changing data; arrays are efficient for fixed-size, homogeneous data.')],
    extended=[('A weather station in Ulaanbaatar records the temperature every hour for 7 days. Describe how this data would be stored in a 2D array and write Python code to find the day with the highest average temperature and the hottest single hour.', 'temps[day][hour] with 7 rows × 24 columns. Loop over days computing sum(temps[d]) / 24, tracking the maximum average and its index; nested loops over d and h to find the maximum reading and its (day, hour). Model code with correct indices, initialisation from temps[0][0], and output.', 6)],
))


@R.add('ch10-st1', 'C3', (1, 5), 'short')
def list_out(rng, slot):
    nums = [rng.randint(1, 20) for _ in range(rng.randint(5, 7))]
    v = rng.choice(['nums', 'data', 'marks', 'scores', 'vals'])
    i = rng.randint(1, len(nums) - 2)
    forms = [f'{v} = {nums}\n{v}.append({nums[0] + 1})\n{v}.insert({i}, 0)\nprint({v}[{i}], {v}[-1], len({v}))',
             f'{v} = {nums}\n{v}.remove({nums[i]})\n{v}.pop()\nprint({v})',
             f'{v} = {nums}\nfor k in range(len({v})):\n    if {v}[k] % 2 == 0:\n        {v}[k] = {v}[k] // 2\nprint({v})',
             f'{v} = {nums}\nprint({v}[1:{i + 2}], {v}[::2])',
             f'{v} = {nums}\nbig = 0\nfor x in {v}:\n    if x > {v}[0]:\n        big += 1\nprint(big)',
             f'{v} = {nums}\n{v}.sort()\nprint({v}[0] + {v}[-1], {v}.index({sorted(nums)[i]}))']
    code = rng.choice(forms if slot.d >= 3 else forms[:4])
    return out_item(rng, code, marks=2 if slot.d <= 3 else 3)


@R.add('ch10-st1', 'C3', (2, 5), 'short')
def grid_out(rng, slot):
    r, c = rng.randint(2, 4), rng.randint(3, 4)
    g = [[rng.randint(0, 9) for _ in range(c)] for _ in range(r)]
    rows = '[' + ', '.join(str(x) for x in g) + ']'
    forms = [f'grid = {rows}\nprint(grid[{r - 1}][{c - 2}], len(grid), len(grid[0]))',
             f'grid = {rows}\nt = 0\nfor row in grid:\n    t += row[{rng.randint(0, c - 1)}]\nprint(t)',
             f'grid = {rows}\nfor i in range(len(grid)):\n    print(sum(grid[i]), end=" ")\nprint()',
             f'grid = {rows}\nbest = grid[0][0]\nfor i in range({r}):\n    for j in range({c}):\n        if grid[i][j] > best:\n            best = grid[i][j]\nprint(best)',
             f'grid = {rows}\ncols = []\nfor j in range({c}):\n    s = 0\n    for i in range({r}):\n        s += grid[i][j]\n    cols.append(s)\nprint(cols)',
             f'grid = {rows}\nd = 0\nfor i in range(min({r}, {c})):\n    d += grid[i][i]\nprint(d)']
    return out_item(rng, rng.choice(forms), marks=3)


K.ar('ch10-st1', [
    ('Accessing nums[i] takes the same time for any valid i.', 'The address of each element can be calculated directly from its index.', 0, 'Both true; R explains A.'),
    ('A Java array\'s length can be increased after it is created.', 'Java arrays are allocated as a fixed block of memory.', 3, 'A false; R true.'),
    ('A 2D array can represent a chess board.', 'A 2D array stores data in rows and columns.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch10-st1', [
    ('Write a Python function row_totals(grid) that returns a list of the sum of each row of a 2D list, and col_max(grid) that returns a list of the largest value in each column.',
     'def row_totals(grid):\n    return [sum(row) for row in grid]\n\ndef col_max(grid):\n    out = []\n    for j in range(len(grid[0])):\n        m = grid[0][j]\n        for i in range(1, len(grid)):\n            if grid[i][j] > m:\n                m = grid[i][j]\n        out.append(m)\n    return out',
     'g = [[3, 8, 1], [7, 2, 9]]\nassert row_totals(g) == [12, 18]\nassert col_max(g) == [7, 8, 9]', 5),
    ('Write a Python function remove_duplicates(items) that returns a new list with duplicates removed while keeping the original order, without using set().',
     'def remove_duplicates(items):\n    out = []\n    for x in items:\n        if x not in out:\n            out.append(x)\n    return out',
     'assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]\nassert remove_duplicates([]) == []', 4),
], d=(3, 5))


R.facts('ch10-st2', F(
    terms=[('stack', 'a last-in, first-out (LIFO) data structure in which items are added and removed only at the top'),
           ('push', 'the stack operation that adds an item to the top'),
           ('pop', 'the stack operation that removes and returns the item at the top'),
           ('peek', 'returning the top item of a stack without removing it'),
           ('stack overflow', 'an error that occurs when pushing onto a full stack (or when the call stack runs out of space)'),
           ('stack underflow', 'an error that occurs when popping from an empty stack'),
           ('call stack', 'the stack used by a program to store return addresses, parameters and local variables for active function calls')],
    facts=[('Which principle does a stack follow?', 'Last in, first out', ['First in, first out', 'Highest priority first', 'Random access'], 'The most recently pushed item is popped first.'),
           ('Which application uses a stack?', 'The undo feature of a text editor', ['A printer queue', 'A breadth-first search', 'Round-robin scheduling'], 'The last action is undone first.'),
           ('After push(4), push(7), pop(), push(2), what is at the top?', '2', ['4', '7', 'The stack is empty'], 'pop removed 7; 2 is then pushed on 4.'),
           ('How is a stack typically implemented with an array?', 'An array plus a top pointer (index of the top item)', ['An array with front and rear pointers', 'Two linked lists', 'A hash table'], 'Only one end is used.')],
    why=[('Explain why a stack is used to check that brackets in an expression are balanced.', 'Each opening bracket is pushed; when a closing bracket appears it must match the most recently opened unmatched bracket, which is exactly the top of the stack (LIFO); if the stack is empty at the end, all are matched.'),
         ('Explain why recursion uses a call stack.', 'Each call must remember its own parameters, local variables and return address; the most recent call must finish first and return to its caller, which is LIFO behaviour.'),
         ('Explain why the program should check isEmpty() before popping.', 'Popping an empty stack causes underflow – there is no item to return – which would crash the program or return invalid data.')],
    contrast=[('push', 'pop', 'push adds an item to the top of the stack; pop removes and returns the item at the top.'),
              ('a stack', 'a queue', 'A stack is LIFO – items are added and removed at the same end (top); a queue is FIFO – items join at the rear and leave from the front.')],
    misc=[('pop() returns the item at the bottom of the stack.', 'pop returns the top item, the one most recently pushed.'),
          ('A stack lets you remove any item directly.', 'Only the top item can be accessed; other items must be popped first.'),
          ('Stack overflow only happens with infinite loops.', 'It happens when a stack is full, e.g. too-deep (often infinite) recursion or pushing onto a full fixed-size stack.')],
    evaluate=[('A stack is the most suitable structure for a web browser\'s history.', ['the back button returns to the most recent page – LIFO', 'push on visit, pop on back'], ['forward navigation needs a second stack', 'a full history list needs random access, not a stack'], 'Two stacks model back/forward well; a list is needed for a searchable history view.')],
    extended=[('Describe how a stack can be used to evaluate the postfix expression 6 2 + 5 * 8 4 / −, showing the stack after each step, and explain why postfix expressions need no brackets.', 'Push 6, push 2; + → pop 2, 6 push 8; push 5; * → 40; push 8, push 4; / → 2; − → 40 − 2 = 38. Stack contents: [6] [6,2] [8] [8,5] [40] [40,8] [40,8,4] [40,2] [38]. Operator order is fixed by position, so precedence and brackets are unnecessary.', 6)],
))


def _stack_ops(rng, n):
    ops, st, log = [], [], []
    for _ in range(n):
        if st and rng.random() < 0.4:
            ops.append('pop()')
            log.append(st.pop())
        elif st and rng.random() < 0.15:
            ops.append('peek()')
            log.append(st[-1])
        else:
            v = rng.randint(1, 50)
            ops.append(f'push({v})')
            st.append(v)
    return ops, st, log


@R.add('ch10-st2', 'C3', (1, 5), 'short')
def stack_trace(rng, slot):
    ops, st, log = _stack_ops(rng, 5 + slot.d)
    if not log:
        return None
    s = rng.choice(['S', 'stack', 'undo'])
    return dict(stem=f'An empty stack {s} undergoes these operations in order: {", ".join(f"{s}.{o}" for o in ops)}. State the values returned by pop() and peek() in order, and the contents of the stack from bottom to top at the end.',
                answer=f'Returned: {", ".join(map(str, log))}; final stack (bottom→top): {st if st else "empty"}', markingKey=f'Returned {", ".join(map(str, log))} (2); final {st if st else "empty"} (1).', marks=3)


@R.add('ch10-st2', 'C3', (2, 5), 'short')
def bracket_check(rng, slot):
    pairs = {')': '(', ']': '[', '}': '{'}
    exprs = ['(a + b) * [c - d]', '{x * (y + z)]', '((a + b) * c', 'arr[i] + f(x)) ', '{[(a)]}', '([)]', 'f(g(h[x]))', 'm = {k: [1, 2}]', 'print((a[0] + b[1]) / 2)', '[(x + y) * {z}']
    e = rng.choice(exprs).strip()
    st, res, pos = [], None, None
    for i, ch in enumerate(e):
        if ch in '([{':
            st.append(ch)
        elif ch in pairs:
            if not st or st[-1] != pairs[ch]:
                res = f'unbalanced – "{ch}" at position {i} does not match ' + (f'"{st[-1]}"' if st else 'anything (stack empty)')
                break
            st.pop()
    if res is None:
        res = 'balanced' if not st else f'unbalanced – {len(st)} unclosed bracket(s) left on the stack: {"".join(st)}'
    return dict(stem=f'A stack-based algorithm checks brackets: push every opening bracket; on a closing bracket pop and check that it matches; at the end the stack must be empty. Apply it to  {e}  (positions start at 0) and state the result.',
                answer=res, markingKey=f'{res}. 1 mark for correct use of the stack, 1 for the result, 1 for identifying where/why it fails (or that the stack ends empty).', marks=3)


@R.add('ch10-st2', 'C3', (3, 5), 'short')
def array_stack(rng, slot):
    size = rng.choice([4, 5])
    ops, st, top, log, err = [], [None] * size, -1, [], None
    for _ in range(7):
        if top >= 0 and rng.random() < 0.4:
            ops.append('pop')
            log.append(st[top]); top -= 1
        else:
            v = rng.randint(1, 99)
            ops.append(f'push {v}')
            if top == size - 1:
                err = f'overflow at "push {v}"'
                break
            top += 1; st[top] = v
    arr = [x if i <= top else '–' for i, x in enumerate(st)]
    return dict(stem=f'A stack is implemented as an array of size {size} with a pointer top, initially −1 (empty). Before each push the program checks for overflow (top = {size - 1}). Trace these operations: {", ".join(ops)}. State the final value of top, the values popped and whether overflow occurred.',
                answer=f'top = {top}; popped {", ".join(map(str, log)) or "none"}; {err or "no overflow"}', markingKey=f'Final live contents {arr} (1); top = {top} (1); popped {log} (1); {err or "no overflow"} (1).', marks=4)


K.ar('ch10-st2', [
    ('A stack is used to reverse the order of items.', 'Items are removed in the opposite order to which they were added.', 0, 'Both true; R explains A.'),
    ('Popping an empty stack causes overflow.', 'Overflow occurs when pushing onto a full stack.', 3, 'A false (it is underflow); R true.'),
    ('Function calls are managed with a stack.', 'The most recently called function must return first.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch10-st2', [
    ('Write a Python class Stack with methods push(x), pop(), peek(), is_empty() and size(), using a list. pop and peek should raise IndexError("stack empty") when the stack is empty.',
     'class Stack:\n    def __init__(self):\n        self._items = []\n    def push(self, x):\n        self._items.append(x)\n    def pop(self):\n        if not self._items:\n            raise IndexError("stack empty")\n        return self._items.pop()\n    def peek(self):\n        if not self._items:\n            raise IndexError("stack empty")\n        return self._items[-1]\n    def is_empty(self):\n        return len(self._items) == 0\n    def size(self):\n        return len(self._items)',
     's = Stack(); s.push(1); s.push(2)\nassert s.peek() == 2 and s.pop() == 2 and s.size() == 1\ns.pop()\nassert s.is_empty()\ntry:\n    s.pop(); raise AssertionError\nexcept IndexError:\n    pass', 5),
    ('Write a Python function reverse_words(sentence) that uses a stack (a list with append/pop only) to return the words of the sentence in reverse order.',
     'def reverse_words(sentence):\n    st = []\n    for w in sentence.split():\n        st.append(w)\n    out = []\n    while st:\n        out.append(st.pop())\n    return " ".join(out)',
     'assert reverse_words("to be or not") == "not or be to"', 4),
], d=(3, 5))


R.facts('ch10-st3', F(
    terms=[('queue', 'a first-in, first-out (FIFO) data structure in which items join at the rear and leave from the front'),
           ('enqueue', 'the queue operation that adds an item to the rear'),
           ('dequeue', 'the queue operation that removes and returns the item at the front'),
           ('circular queue', 'a queue stored in a fixed-size array in which the front and rear pointers wrap around to the start, reusing freed space'),
           ('priority queue', 'a queue in which each item has a priority and the highest-priority item is removed first'),
           ('front pointer', 'the index of the item that will be dequeued next')],
    facts=[('Which principle does a queue follow?', 'First in, first out', ['Last in, first out', 'Smallest first', 'Random order'], 'The earliest item added is removed first.'),
           ('Which application uses a queue?', 'Print jobs waiting for a shared printer', ['Undo in a word processor', 'Checking balanced brackets', 'The call stack'], 'Jobs are printed in arrival order.'),
           ('After enqueue(3), enqueue(8), dequeue(), enqueue(5), what is at the front?', '8', ['3', '5', 'The queue is empty'], '3 left first.'),
           ('Why is a circular queue more efficient than a simple linear array queue?', 'Space freed at the front can be reused without shifting elements', ['It never becomes full', 'It sorts the items', 'It uses no pointers'], 'Pointers wrap around using modulo arithmetic.')],
    why=[('Explain why a queue is suitable for managing requests to a web server.', 'Requests should be served fairly in the order they arrive; a FIFO queue ensures the earliest request is handled first and buffers requests that arrive while the server is busy.'),
         ('Explain why a circular queue uses the modulo operator when moving its pointers.', 'When the rear (or front) reaches the last index of the array it must wrap to index 0; (pointer + 1) mod size achieves this so free cells at the start are reused.'),
         ('Explain why a priority queue is used for hospital emergency triage software.', 'Patients must be seen according to urgency, not arrival time; a priority queue always returns the most urgent patient next, with FIFO order among equal priorities.')],
    contrast=[('a linear queue', 'a circular queue', 'In a linear array queue the rear only moves forward, so freed cells at the front are wasted (or items must be shifted); a circular queue wraps the pointers around to reuse those cells.'),
              ('a queue', 'a priority queue', 'A queue removes items strictly in arrival order; a priority queue removes the item with the highest priority first, regardless of arrival.')],
    misc=[('Dequeue removes the most recently added item.', 'Dequeue removes the oldest item at the front; the most recent is at the rear.'),
          ('A circular queue can never be full.', 'It has a fixed size; it is full when every cell holds an item (count = size).'),
          ('Python lists are the most efficient way to dequeue from the front.', 'list.pop(0) shifts every element (O(n)); collections.deque.popleft() is O(1).')],
    evaluate=[('A simple FIFO queue is fair for scheduling processes on a CPU.', ['every process eventually runs, in arrival order', 'simple and predictable'], ['long jobs delay short ones (convoy effect)', 'ignores urgency and interactivity', 'priority/multilevel queues give better response'], 'FIFO is fair in order but not in response time; real schedulers use priority or round-robin queues.')],
    extended=[('A circular queue of size 5 is used to buffer keystrokes. Explain how front, rear and count are updated on enqueue and dequeue, and how the program detects full and empty states. Illustrate with a sequence of operations that wraps around.', 'enqueue: if count = 5 full; rear = (rear + 1) mod 5; arr[rear] = x; count += 1. dequeue: if count = 0 empty; x = arr[front]; front = (front + 1) mod 5; count −= 1. Example: enqueue a-e (rear 4), dequeue twice (front 2), enqueue f, g → rear wraps to 0, 1; queue holds c d e f g.', 6)],
))


@R.add('ch10-st3', 'C3', (1, 5), 'short')
def queue_trace(rng, slot):
    q, ops, log = deque(), [], []
    for _ in range(5 + slot.d):
        if q and rng.random() < 0.4:
            ops.append('dequeue()'); log.append(q.popleft())
        else:
            v = rng.choice(PEOPLE)
            if v in q:
                continue
            ops.append(f'enqueue("{v}")'); q.append(v)
    if not log:
        return None
    return dict(stem=f'An empty queue Q undergoes: {", ".join(f"Q.{o}" for o in ops)}. State the values returned by dequeue() in order and the final contents of the queue from front to rear.',
                answer=f'Dequeued: {", ".join(log)}; final (front→rear): {list(q) if q else "empty"}', markingKey=f'Dequeued {", ".join(log)} (2); final {list(q) if q else "empty"} (1).', marks=3)


@R.add('ch10-st3', 'C3', (2, 5), 'short')
def circ_queue(rng, slot):
    size = rng.choice([4, 5, 6])
    arr, front, rear, count, ops, log = [None] * size, 0, -1, 0, [], []
    for _ in range(8 + slot.d):
        if count and rng.random() < 0.45:
            ops.append('dequeue')
            log.append(arr[front]); front = (front + 1) % size; count -= 1
        elif count < size:
            v = rng.randint(10, 99)
            ops.append(f'enqueue {v}')
            rear = (rear + 1) % size; arr[rear] = v; count += 1
    return dict(stem=f'A circular queue uses an array of size {size} with front = 0, rear = −1 and count = 0 initially. enqueue does rear ← (rear + 1) mod {size}; dequeue does front ← (front + 1) mod {size}. Trace: {", ".join(ops)}. State the final values of front, rear and count, the items dequeued, and the items in the queue from front to rear.',
                answer=f'front = {front}, rear = {rear}, count = {count}; dequeued {", ".join(map(str, log)) or "none"}; queue {[arr[(front + i) % size] for i in range(count)]}',
                markingKey=f'front {front}, rear {rear}, count {count} (1 each); dequeued {log} (1); contents {[arr[(front + i) % size] for i in range(count)]} (1).', marks=5)


@R.add('ch10-st3', 'C3', (2, 5), 'short')
def prio_queue(rng, slot):
    names = rng.sample(PEOPLE, 5)
    pr = [rng.randint(1, 4) for _ in names]
    order = [n for _, i, n in sorted((p, i, n) for i, (n, p) in enumerate(zip(names, pr)))]
    arrivals = ', '.join(f'{n} (priority {p})' for n, p in zip(names, pr))
    k = rng.randint(2, 4)
    return dict(stem=f'Patients arrive at an emergency department in this order: {arrivals}. A priority queue serves priority 1 first and patients with equal priority in arrival order. State the order in which the first {k} patients are seen, and explain why a normal FIFO queue would be unsuitable.',
                answer=f'{", ".join(order[:k])}; a FIFO queue ignores urgency', markingKey=f'Order {", ".join(order[:k])} (2); FIFO would treat {names[0]} first regardless of urgency, endangering urgent patients (1).', marks=3)


K.ar('ch10-st3', [
    ('A printer spooler uses a queue.', 'Documents should be printed in the order they were sent.', 0, 'Both true; R explains A.'),
    ('In a circular queue the rear pointer can be smaller than the front pointer.', 'The pointers wrap around to the start of the array.', 0, 'Both true; R explains A.'),
    ('Dequeue returns the newest item in a queue.', 'Queues are first-in, first-out.', 3, 'A false; R true.'),
])

K.code_tasks('ch10-st3', [
    ('Write a Python class CircularQueue(size) with enqueue(x) (return False if full), dequeue() (return None if empty), is_empty() and is_full(), using a fixed-size list and front, rear and count attributes.',
     'class CircularQueue:\n    def __init__(self, size):\n        self.size = size\n        self.arr = [None] * size\n        self.front, self.rear, self.count = 0, -1, 0\n    def is_empty(self):\n        return self.count == 0\n    def is_full(self):\n        return self.count == self.size\n    def enqueue(self, x):\n        if self.is_full():\n            return False\n        self.rear = (self.rear + 1) % self.size\n        self.arr[self.rear] = x\n        self.count += 1\n        return True\n    def dequeue(self):\n        if self.is_empty():\n            return None\n        x = self.arr[self.front]\n        self.front = (self.front + 1) % self.size\n        self.count -= 1\n        return x',
     'q = CircularQueue(3)\nassert q.enqueue(1) and q.enqueue(2) and q.enqueue(3) and not q.enqueue(4)\nassert q.dequeue() == 1\nassert q.enqueue(4)\nassert [q.dequeue(), q.dequeue(), q.dequeue(), q.dequeue()] == [2, 3, 4, None]', 6),
], d=(4, 5))


R.facts('ch10-st4', F(
    terms=[('data structure', 'a way of organising and storing data so that it can be accessed and modified efficiently for a particular purpose'),
           ('dictionary (hash map)', 'a structure that stores key-value pairs and gives very fast lookup by key'),
           ('set', 'an unordered collection of unique items with fast membership testing'),
           ('record (struct)', 'a structure that groups related fields of possibly different types, such as a student\'s name, age and grade'),
           ('time complexity', 'a measure of how the running time of an operation grows as the amount of data grows'),
           ('tuple', 'an ordered, immutable sequence of values')],
    facts=[('Which structure gives the fastest lookup of a student\'s record by student ID?', 'Dictionary keyed by ID', ['Unsorted list', 'Stack', 'Queue'], 'Hash lookup is O(1) on average.'),
           ('Which structure is best for the "back" button of a browser?', 'Stack', ['Queue', 'Set', '2D array'], 'Most recent page first.'),
           ('Which structure automatically prevents duplicate entries?', 'Set', ['List', 'Queue', 'Array'], 'Sets hold unique items.'),
           ('Which structure best represents a 9 × 9 Sudoku grid?', '2D array', ['Queue', 'Stack', 'Set'], 'Rows and columns map directly.')],
    why=[('Explain why choosing an appropriate data structure affects a program\'s performance.', 'Different structures make different operations fast or slow: e.g. lookup by key is O(1) in a dictionary but O(n) in a list, insertion at the front is O(1) in a deque but O(n) in a list; the right choice matches the most frequent operations.'),
         ('Explain why a dictionary is better than two parallel lists for storing country names and capitals.', 'A dictionary links each key directly to its value, so lookup is fast and the pairing cannot get out of step; parallel lists require searching and must be updated together.'),
         ('Explain why a set is useful for checking whether a username is already taken.', 'Membership testing in a set is O(1) on average regardless of size, and the set automatically stores each username once.')],
    contrast=[('a list', 'a dictionary', 'A list stores items in order accessed by integer index (search by value is O(n)); a dictionary stores key-value pairs accessed by key in O(1) average time.'),
              ('a list', 'a set', 'A list is ordered and allows duplicates; a set is unordered, holds unique items and gives fast membership tests.')],
    misc=[('A list is always the best choice because it can hold anything.', 'Lists are flexible, but lookups by value are slow; dictionaries, sets, stacks or queues may be far more efficient for particular operations.'),
          ('Sets keep items in the order they were added.', 'Sets are unordered collections (iteration order is not guaranteed to be insertion order).'),
          ('Dictionaries can have two identical keys with different values.', 'Keys are unique; assigning to an existing key replaces its value.')],
    evaluate=[('A dictionary should be used for every collection of data in Python.', ['very fast key lookup', 'flexible'], ['uses more memory than a list', 'no natural order for sequences or positions', 'keys must be hashable'], 'Dictionaries suit key-based lookups; ordered sequences, stacks and queues need other structures.')],
    extended=[('A ride-hailing app in Jakarta must (a) store each driver\'s details by driver ID, (b) hold ride requests in arrival order, (c) remember the last screens a user visited for the back button, and (d) record which drivers are currently online. Choose a data structure for each, justify the choices with reference to the operations needed, and comment on efficiency.', '(a) dictionary keyed by driver ID – O(1) lookup/update; (b) queue (deque) – FIFO enqueue/dequeue O(1); (c) stack – LIFO push/pop; (d) set of driver IDs – unique, O(1) add/remove/membership. Justifications must link each structure to its operations and efficiency.', 6)],
))


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def ds_choice(rng, slot):
    items = [('the order of moves so that a chess app can undo the last move', 'stack', 'undo needs the most recent move first (LIFO)'),
             ('customers waiting to speak to a call-centre agent', 'queue', 'customers must be served in arrival order (FIFO)'),
             ('the price of each product, looked up by barcode', 'dictionary', 'fast O(1) lookup of a value by its key'),
             ('the unique words appearing in a book', 'set', 'duplicates are ignored and membership tests are fast'),
             ('daily rainfall for each day of each month of a year', '2D array', 'naturally indexed by month and day'),
             ('the top 10 high scores in sorted order', 'sorted list (array)', 'small, ordered and accessed by position'),
             ('tasks for a robot, where urgent tasks must be done first', 'priority queue', 'items are removed according to priority'),
             ('a student\'s name, date of birth and grade kept together', 'record / object', 'groups related fields of different types')]
    who, ds, why = rng.choice(items)
    return dict(stem=f'State the most appropriate data structure for storing {who}, and justify your choice.', answer=f'{ds}: {why}.', markingKey=f'{ds} (1); justification: {why} (1-2).', marks=3)


@R.add('ch10-st4', 'C3', (2, 5), 'short')
def dict_out(rng, slot):
    keys = rng.sample(['Lima', 'Oslo', 'Accra', 'Hanoi', 'Quito', 'Seoul', 'Doha'], 4)
    vals = rng.sample(range(1, 31), len(keys))
    d = dict(zip(keys, vals))
    k2 = rng.choice(keys)
    forms = [f'stock = {d}\nstock["{k2}"] += 5\nstock["Rome"] = 2\nprint(len(stock), stock["{k2}"], stock.get("Paris", 0))',
             f'stock = {d}\ntotal = 0\nfor city, n in stock.items():\n    if n > {sorted(vals)[1]}:\n        total += n\nprint(total)',
             f'stock = {d}\nbest = max(stock, key=stock.get)\nprint(best, stock[best])',
             f'seen = set()\nfor w in {[rng.choice(keys) for _ in range(6)]}:\n    seen.add(w)\nprint(len(seen), "{k2}" in seen)']
    return out_item(rng, rng.choice(forms), marks=2 if slot.d <= 3 else 3)


K.ar('ch10-st4', [
    ('Looking up a value by key in a dictionary is usually faster than searching a list.', 'Dictionaries use hashing to locate keys directly.', 0, 'Both true; R explains A.'),
    ('A queue is the best structure for an undo feature.', 'A queue removes the oldest item first.', 3, 'A false (a stack is needed); R true.'),
    ('A set cannot contain duplicate values.', 'Adding an existing value to a set has no effect.', 0, 'Both true; R illustrates/explains A.'),
])


# =============================================================================================
# ch11 B2.4 Algorithms and efficiency
# =============================================================================================
R.facts('ch11-st1', F(
    terms=[('Big O notation', 'a notation that describes how the running time or memory use of an algorithm grows in the worst case as the input size n grows, ignoring constants'),
           ('O(1) – constant time', 'running time that does not depend on the input size'),
           ('O(n) – linear time', 'running time that grows in direct proportion to the input size'),
           ('O(n²) – quadratic time', 'running time proportional to the square of the input size, typical of nested loops over the data'),
           ('O(log n) – logarithmic time', 'running time that grows by a constant amount each time the input size doubles, typical of halving algorithms such as binary search'),
           ('space complexity', 'how the amount of memory an algorithm needs grows with the input size'),
           ('worst case', 'the input of a given size for which an algorithm takes the longest time')],
    facts=[('What is the time complexity of accessing an element of an array by index?', 'O(1)', ['O(n)', 'O(log n)', 'O(n²)'], 'Address calculation is constant time.'),
           ('A loop runs from 1 to n with a nested loop also running from 1 to n. Its complexity is…', 'O(n²)', ['O(n)', 'O(2n)', 'O(log n)'], 'n × n iterations.'),
           ('Which complexity grows the slowest as n increases?', 'O(log n)', ['O(n)', 'O(n log n)', 'O(n²)'], 'Doubling n adds only one step.'),
           ('If an O(n²) algorithm takes 2 s for n = 1000, roughly how long for n = 2000?', '8 s', ['4 s', '2 s', '16 s'], 'Doubling n multiplies time by 2² = 4.')],
    why=[('Explain why Big O notation ignores constant factors and lower-order terms.', 'For large n the highest-order term dominates the growth (e.g. n² outgrows 100n), and constants depend on hardware and implementation; Big O describes how the algorithm scales, which is what matters for large inputs.'),
         ('Explain why an O(n log n) sorting algorithm is preferred to an O(n²) one for a million items.', 'For n = 10^6, n² = 10^12 operations while n log₂ n ≈ 2 × 10^7, so the O(n log n) algorithm is roughly 50 000 times faster; the gap widens as n grows.'),
         ('Explain why an algorithm with a better Big O can be slower for small inputs.', 'Big O hides constant factors and overheads; for small n a simple O(n²) algorithm with little overhead can beat a complex O(n log n) one, which is why hybrid sorts switch to insertion sort for small sub-arrays.')],
    contrast=[('time complexity', 'space complexity', 'Time complexity describes how running time grows with input size; space complexity describes how memory usage grows.'),
              ('O(n)', 'O(log n)', 'O(n) time grows in proportion to n (e.g. linear search); O(log n) time grows by one step each time n doubles (e.g. binary search), so it is far faster for large n.')],
    misc=[('An O(n) algorithm always runs faster than an O(n²) algorithm.', 'Big O describes growth for large n; for small inputs constant factors may make the O(n²) algorithm faster.'),
          ('O(2n) is a different complexity class from O(n).', 'Constants are dropped: O(2n) = O(n).'),
          ('Big O gives the exact number of seconds an algorithm takes.', 'Big O describes the growth rate, not actual time, which depends on hardware and implementation.')],
    evaluate=[('Big O notation is the only thing that matters when choosing an algorithm.', ['predicts scalability for large inputs'], ['constants and real data sizes matter', 'memory use, simplicity and stability also matter', 'average case may differ from worst case'], 'Big O is a key guide for large data, but practical choice also weighs constants, memory, data characteristics and maintainability.')],
    extended=[('A social-media start-up in Lagos checks whether a new username is already taken. Compare storing usernames in an unsorted list, a sorted list and a hash set, giving the Big O complexity of checking and inserting in each case, and recommend a structure for 50 million users.', 'Unsorted list: check O(n), insert O(1) (append). Sorted list: check O(log n) by binary search, insert O(n) (shift). Hash set: check and insert O(1) average. For 50 million users: n = 5 × 10^7 comparisons vs ~26 vs ~1; recommend a hash set (or database index), noting memory use and worst-case collisions.', 6)],
))


def _ops_count(kind, n):
    c = 0
    if kind == 'single':
        for i in range(n):
            c += 1
    elif kind == 'nested':
        for i in range(n):
            for j in range(n):
                c += 1
    elif kind == 'tri':
        for i in range(n):
            for j in range(i + 1, n):
                c += 1
    elif kind == 'halve':
        i = n
        while i > 1:
            i //= 2; c += 1
    elif kind == 'nested_log':
        for i in range(n):
            j = 1
            while j < n:
                j *= 2; c += 1
    elif kind == 'two':
        for i in range(n):
            c += 1
        for j in range(n):
            c += 1
    return c


_OPS_CODE = {'single': ('for i in range(n):\n    count += 1', 'O(n)'),
             'nested': ('for i in range(n):\n    for j in range(n):\n        count += 1', 'O(n²)'),
             'tri': ('for i in range(n):\n    for j in range(i + 1, n):\n        count += 1', 'O(n²)'),
             'halve': ('i = n\nwhile i > 1:\n    i = i // 2\n    count += 1', 'O(log n)'),
             'nested_log': ('for i in range(n):\n    j = 1\n    while j < n:\n        j = j * 2\n        count += 1', 'O(n log n)'),
             'two': ('for i in range(n):\n    count += 1\nfor j in range(n):\n    count += 1', 'O(n)')}


@R.add('ch11-st1', 'C3', (1, 5), 'short')
def big_o_code(rng, slot):
    kind = rng.choice(list(_OPS_CODE))
    n = rng.choice([8, 16, 20, 32, 64, 100])
    code, bo = _OPS_CODE[kind]
    full = f'n = {n}\ncount = 0\n{code}\nprint(count)'
    out = run_py(full)
    assert int(out) == _ops_count(kind, n)
    return dict(stem=f'State the output of this code and the time complexity of the loop structure in Big O notation.\n{full}', answer=f'{out}; {bo}',
                markingKey=f'Output {out} (1); {bo} (1) with justification, e.g. number of iterations as a function of n (1).', marks=3)


@R.add('ch11-st1', 'C3', (2, 5), 'numerical')
def scale_time(rng, slot):
    bo, f = rng.choice([('O(n)', lambda r: r), ('O(n²)', lambda r: r * r), ('O(n³)', lambda r: r ** 3), ('O(log n)', None), ('O(n log n)', None)])
    t = rng.choice([0.5, 1, 2, 4, 5])
    n1 = rng.choice([1000, 2000, 5000, 10000])
    k = rng.choice([2, 4, 10])
    n2 = n1 * k
    if bo == 'O(log n)':
        t2 = t * math.log2(n2) / math.log2(n1)
    elif bo == 'O(n log n)':
        t2 = t * (n2 * math.log2(n2)) / (n1 * math.log2(n1))
    else:
        t2 = t * f(k)
    return dict(stem=f'An algorithm with time complexity {bo} takes {t} s to process {n1:,} items. Estimate the time to process {n2:,} items, stating any assumption.',
                answer=f'≈ {r2(t2, 2)} s', markingKey=f'Time ∝ {bo[2:-1]}, so T({n2:,}) = T({n1:,}) × ratio of {bo[2:-1]} values = {t} × {r2(t2 / t, 3)} (M1) = {r2(t2, 2)} s (A1); assumption: the constant factor is unchanged and the same (worst) case applies (R1).', marks=3)


@R.add('ch11-st1', 'C1', (1, 3), 'mcq')
def big_o_mcq(rng, slot):
    items = [('binary search on a sorted array', 'O(log n)'), ('linear search on an unsorted array', 'O(n)'), ('bubble sort in the worst case', 'O(n²)'),
             ('accessing an array element by index', 'O(1)'), ('merge sort', 'O(n log n)'), ('printing every pair of items in a list', 'O(n²)'),
             ('pushing onto a stack', 'O(1)'), ('finding the maximum in an unsorted list', 'O(n)')]
    what, a = rng.choice(items)
    return nmcq(rng, f'What is the time complexity of {what}?', a, ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)'], f'{what}: {a}.')


K.ar('ch11-st1', [
    ('Binary search is O(log n).', 'Each comparison halves the number of items still to be searched.', 0, 'Both true; R explains A.'),
    ('O(3n + 5) simplifies to O(n).', 'Big O ignores constant factors and lower-order terms.', 0, 'Both true; R explains A.'),
    ('An O(n²) algorithm takes twice as long when n doubles.', 'Nested loops over n items perform n² operations.', 3, 'A false (four times as long); R true.'),
])


R.facts('ch11-st2', F(
    terms=[('linear search', 'a search that checks each element in turn from the start until the target is found or the end is reached'),
           ('binary search', 'a search of a sorted list that repeatedly compares the target with the middle element and discards the half that cannot contain it'),
           ('sorted data', 'data arranged in order (ascending or descending), required by binary search'),
           ('midpoint', 'in binary search, the index (low + high) div 2 of the element compared with the target'),
           ('sequential access', 'accessing items one after another in order, as linear search does')],
    facts=[('What is the maximum number of comparisons binary search needs for 1000 sorted items?', '10', ['1000', '500', '32'], '2^10 = 1024 ≥ 1000.'),
           ('Which condition is required for binary search?', 'The data must be sorted', ['The data must be numeric', 'The list must have an even length', 'The target must be in the list'], 'Halving relies on order.'),
           ('In the worst case, how many comparisons does linear search make on n items?', 'n', ['log₂ n', 'n/2', '1'], 'The target is last or absent.'),
           ('When is linear search preferable to binary search?', 'For small or unsorted lists that are searched only once', ['For very large sorted arrays', 'Never', 'When the data is already sorted and searched often'], 'Sorting first costs more than one linear search.')],
    why=[('Explain why binary search is much faster than linear search for large sorted lists.', 'Each comparison halves the remaining search space, so at most about log₂ n comparisons are needed (20 for a million items) instead of up to n for linear search.'),
         ('Explain why binary search cannot be used on an unsorted list.', 'Discarding half the list assumes all items on that side are larger (or smaller) than the middle; without order the target could be in the discarded half.'),
         ('Explain why sorting a list just to perform one search may not be worthwhile.', 'Sorting costs at least O(n log n), more than a single O(n) linear search; sorting only pays off if the list is searched many times.')],
    contrast=[('linear search', 'binary search', 'Linear search checks items one by one, works on unsorted data and is O(n); binary search needs sorted data, repeatedly halves the search range and is O(log n).')],
    misc=[('Binary search starts by checking the first element.', 'Binary search starts with the middle element of the sorted range.'),
          ('Linear search needs the list to be sorted.', 'Linear search works on any list; sorting can only help it stop early if the target is missing.'),
          ('Binary search on 1 million items needs about 500 000 comparisons.', 'It needs at most about 20, because 2^20 ≈ 1 million.')],
    evaluate=[('Binary search should always be used instead of linear search.', ['O(log n) is far faster on large sorted data'], ['requires sorted data, and keeping it sorted costs time', 'linked lists do not support fast access to the middle', 'linear search is simpler and fine for small lists'], 'Binary search is best for large, sorted, randomly accessible data searched repeatedly; otherwise linear search may be adequate.')],
    extended=[('A pharmacy in Lisbon keeps 20 000 product codes. Compare linear and binary search for looking up a code, calculating the worst-case comparisons for each, and discuss how often the list changes affects the choice.', 'Linear: up to 20 000 comparisons; binary: ⌈log₂ 20 001⌉ = 15. Binary search needs the codes kept sorted; if products are added rarely, sorting/insertion cost is small and binary search is far better; if the list changes constantly, a hash table or database index may be better still.', 6)],
))


def _bsearch(arr, t):
    lo, hi, trace = 0, len(arr) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        trace.append((lo, hi, mid, arr[mid]))
        if arr[mid] == t:
            return mid, trace
        if arr[mid] < t:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, trace


@R.add('ch11-st2', 'C3', (1, 5), 'short')
def bsearch_trace(rng, slot):
    n = 7 + slot.d * 2
    arr = sorted(rng.sample(range(1, 99), n))
    t = rng.choice(arr) if rng.random() < 0.75 else rng.choice([x for x in range(1, 99) if x not in arr])
    pos, tr = _bsearch(arr, t)
    rows = '; '.join(f'low={a}, high={b}, mid={c} (value {d})' for a, b, c, d in tr)
    return dict(stem=f'Binary search (mid = (low + high) div 2, indices from 0) is used to find {t} in the sorted array {arr}. List the values of low, high and mid at each comparison and state the result and the number of comparisons.',
                answer=f'{rows}; {"found at index " + str(pos) if pos >= 0 else "not found (low > high)"}; {len(tr)} comparisons',
                markingKey=f'{rows} (1 mark per correct step, max 3); result {"index " + str(pos) if pos >= 0 else "not found"} (1); {len(tr)} comparisons (1).', marks=5)


@R.add('ch11-st2', 'C3', (1, 4), 'numerical')
def search_compare(rng, slot):
    n = rng.choice([100, 1000, 5000, 65536, 10 ** 6, 3 * 10 ** 6])
    b = math.ceil(math.log2(n + 1))
    return dict(stem=f'A sorted list contains {n:,} items. State the maximum number of comparisons needed to find an item with linear search and with binary search, and the average for linear search when the item is present.',
                answer=f'Linear: {n:,} (average ≈ {r2((n + 1) / 2, 1)}); binary: {b}', markingKey=f'Linear worst {n:,} (1); average (n + 1)/2 ≈ {r2((n + 1) / 2, 1)} (1); binary ⌈log₂({n:,} + 1)⌉ = {b} (1).', marks=3)


@R.add('ch11-st2', 'C3', (1, 4), 'short')
def lsearch_out(rng, slot):
    arr = [rng.randint(1, 30) for _ in range(8)]
    t = rng.choice(arr + [31, 40])
    code = f'data = {arr}\ntarget = {t}\ni = 0\nfound = False\nwhile i < len(data) and not found:\n    if data[i] == target:\n        found = True\n    else:\n        i += 1\nprint(found, i)'
    return out_item(rng, code, marks=2, note='The loop stops at the first match; if not found, i equals len(data).')


K.ar('ch11-st2', [
    ('Binary search requires sorted data.', 'Binary search discards half of the remaining items after each comparison.', 0, 'Both true; R explains why sorting is needed.'),
    ('Linear search is O(log n).', 'Linear search may have to check every element.', 3, 'A false (it is O(n)); R true.'),
    ('Binary search is faster than linear search on large sorted lists.', 'Binary search can be written as a recursive function.', 1, 'Both true, but being recursive is not why it is faster – halving the search range is.'),
])

K.code_tasks('ch11-st2', [
    ('Write a Python function binary_search(arr, target) that returns the index of target in the sorted list arr, or −1 if it is absent, using an iterative loop.',
     'def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1',
     'a = [2, 5, 8, 12, 16, 23, 38]\nassert binary_search(a, 23) == 5 and binary_search(a, 2) == 0 and binary_search(a, 7) == -1 and binary_search([], 1) == -1', 5),
    ('Write a Python function find_all(items, target) that uses linear search to return a list of every index at which target occurs.',
     'def find_all(items, target):\n    out = []\n    for i in range(len(items)):\n        if items[i] == target:\n            out.append(i)\n    return out',
     'assert find_all([3, 1, 3, 4, 3], 3) == [0, 2, 4]\nassert find_all([1, 2], 5) == []', 3),
], d=(3, 5))


R.facts('ch11-st3', F(
    terms=[('bubble sort', 'a sorting algorithm that repeatedly steps through the list comparing adjacent pairs and swapping them if they are in the wrong order, so the largest values "bubble" to the end'),
           ('selection sort', 'a sorting algorithm that repeatedly finds the smallest remaining element and swaps it into the next position of the sorted part'),
           ('pass', 'one complete traversal of the unsorted part of the list during a sort'),
           ('swap', 'exchanging the positions of two elements, usually with a temporary variable'),
           ('in-place sort', 'a sort that rearranges the elements within the original array using only a constant amount of extra memory'),
           ('stable sort', 'a sort that keeps equal elements in their original relative order')],
    facts=[('After the first pass of an ascending bubble sort, which element is guaranteed to be in its final position?', 'The largest element, at the end', ['The smallest element, at the start', 'The middle element', 'None of them'], 'The largest value is carried to the end.'),
           ('How many comparisons does a simple bubble sort make on n items (without early exit)?', 'n(n − 1)/2', ['n', 'n log n', '2n'], '(n − 1) + (n − 2) + … + 1.'),
           ('Which sort makes at most n − 1 swaps?', 'Selection sort', ['Bubble sort', 'Both make n² swaps', 'Neither'], 'One swap per pass.'),
           ('What is the best-case complexity of bubble sort with an early-exit flag on an already sorted list?', 'O(n)', ['O(n²)', 'O(log n)', 'O(1)'], 'One pass with no swaps, then it stops.')],
    why=[('Explain why bubble sort with a "swapped" flag can finish early.', 'If a complete pass makes no swaps, every adjacent pair is in order, so the whole list is sorted and further passes are unnecessary; the flag detects this and stops the loop.'),
         ('Explain why selection sort performs fewer swaps than bubble sort.', 'Selection sort scans to find the minimum and then performs a single swap per pass (at most n − 1 swaps), whereas bubble sort may swap at every comparison.'),
         ('Explain why both bubble sort and selection sort are O(n²).', 'Each uses nested loops: about n passes, each comparing up to n items, giving roughly n²/2 comparisons, which grows quadratically.')],
    contrast=[('bubble sort', 'selection sort', 'Bubble sort compares and swaps adjacent pairs, moving the largest to the end each pass (can stop early, stable); selection sort finds the minimum of the unsorted part and swaps it into place (fewer swaps, not stable, no early exit).')],
    misc=[('Bubble sort always needs n passes.', 'With an early-exit flag it can stop as soon as a pass makes no swaps; at most n − 1 passes are needed.'),
          ('Selection sort is O(n) because it does only n swaps.', 'It still makes about n²/2 comparisons, so it is O(n²).'),
          ('After the first pass of selection sort the largest item is at the end.', 'Ascending selection sort places the smallest item at the start after the first pass.')],
    evaluate=[('Bubble sort should never be used.', ['O(n²) is too slow for large data', 'better algorithms exist (merge sort, quicksort)'], ['simple to code and understand', 'efficient for very small or nearly sorted lists with early exit', 'in-place and stable'], 'Rarely the best choice in practice, but useful for teaching and tiny or nearly sorted datasets.')],
    extended=[('Compare bubble sort and selection sort for sorting 10 exam scores on a microcontroller with very little memory and slow writes to memory, using the number of comparisons and swaps to justify your recommendation.', 'Both in place (O(1) extra memory) and n(n − 1)/2 = 45 comparisons. Bubble sort may perform up to 45 swaps (3 writes each); selection sort at most 9 swaps. With slow writes selection sort is better; bubble sort wins only if the data is nearly sorted (early exit after one pass of 9 comparisons).', 6)],
))


def _bubble_passes(a):
    a = a[:]
    passes, comps, swaps = [], 0, 0
    n = len(a)
    for i in range(n - 1):
        sw = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; swaps += 1; sw = True
        passes.append(a[:])
        if not sw:
            break
    return passes, comps, swaps


def _selection_passes(a):
    a = a[:]
    passes, comps, swaps = [], 0, 0
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]; swaps += 1
        passes.append(a[:])
    return passes, comps, swaps


@R.add('ch11-st3', 'C3', (1, 5), 'short')
def sort_passes(rng, slot):
    n = 5 if slot.d <= 2 else 6 if slot.d <= 4 else 7
    arr = rng.sample(range(1, 60), n)
    alg = rng.choice(['bubble', 'selection'])
    passes, comps, swaps = (_bubble_passes if alg == 'bubble' else _selection_passes)(arr)
    k = min(len(passes), 2 if slot.d <= 2 else 3)
    desc = 'bubble sort (with early exit when a pass makes no swaps)' if alg == 'bubble' else 'selection sort'
    stem = f'The list {arr} is sorted into ascending order using {desc}. Show the list after each of the first {k} passes'
    ans = '; '.join(f'pass {i + 1}: {p}' for i, p in enumerate(passes[:k]))
    key = ans + '. 1 mark per correct pass.'
    m = k
    if slot.d >= 3:
        stem += ', and state the total number of comparisons and swaps needed to sort the list completely'
        ans += f'; {comps} comparisons, {swaps} swaps'
        key += f' Totals: {comps} comparisons, {swaps} swaps ({len(passes)} passes) (1 each).'
        m += 2
    return dict(stem=stem + '.', answer=ans, markingKey=key, marks=m)


@R.add('ch11-st3', 'C3', (2, 5), 'short')
def sort_identify(rng, slot):
    arr = rng.sample(range(1, 60), 6)
    alg = rng.choice(['bubble', 'selection'])
    passes, _, _ = (_bubble_passes if alg == 'bubble' else _selection_passes)(arr)
    other, _, _ = (_selection_passes if alg == 'bubble' else _bubble_passes)(arr)
    if passes[0] == other[0]:
        return None
    return dict(stem=f'The list {arr} is being sorted into ascending order. After the first pass it is {passes[0]}. Identify whether bubble sort or selection sort is being used, and justify your answer.',
                answer=f'{alg.title()} sort', markingKey=(f'Bubble sort (1): the largest value {max(arr)} has moved to the end and other values have shifted one place by adjacent swaps (1-2); selection sort would give {other[0]}.' if alg == 'bubble' else f'Selection sort (1): the smallest value {min(arr)} has been swapped into position 0 with a single swap and the rest are unchanged (1-2); bubble sort would give {other[0]}.'), marks=3)


K.ar('ch11-st3', [
    ('After each pass of an ascending bubble sort, the largest unsorted element reaches its final position.', 'Adjacent comparisons carry the largest value along to the end of the unsorted part.', 0, 'Both true; R explains A.'),
    ('Selection sort can stop early if the list is already sorted.', 'Selection sort scans the whole unsorted part to find the minimum on every pass.', 3, 'A false (it always does all passes); R true.'),
    ('Bubble sort and selection sort are both O(n²).', 'Both sort the list in place.', 1, 'Both true, but being in place does not explain their time complexity.'),
])

K.code_tasks('ch11-st3', [
    ('Write a Python function bubble_sort(arr) that sorts a list in ascending order in place using bubble sort with an early-exit flag, and returns the number of passes made.',
     'def bubble_sort(arr):\n    n = len(arr)\n    passes = 0\n    for i in range(n - 1):\n        swapped = False\n        passes += 1\n        for j in range(n - 1 - i):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return passes',
     'a = [5, 1, 4, 2, 8]\np = bubble_sort(a)\nassert a == [1, 2, 4, 5, 8] and p == 3\nb = [1, 2, 3]\nassert bubble_sort(b) == 1', 5),
    ('Write a Python function selection_sort(arr) that sorts a list into descending order in place using selection sort.',
     'def selection_sort(arr):\n    for i in range(len(arr) - 1):\n        m = i\n        for j in range(i + 1, len(arr)):\n            if arr[j] > arr[m]:\n                m = j\n        arr[i], arr[m] = arr[m], arr[i]',
     'a = [3, 9, 1, 7]\nselection_sort(a)\nassert a == [9, 7, 3, 1]', 4),
], d=(3, 5))


R.facts('ch11-st4', F(
    terms=[('recursion', 'a technique in which a function calls itself to solve smaller instances of the same problem'),
           ('base case', 'the condition in a recursive function that returns a result without making a further recursive call, stopping the recursion'),
           ('recursive case', 'the part of a recursive function that calls itself with a smaller or simpler argument'),
           ('stack overflow (recursion)', 'an error that occurs when recursion is too deep and the call stack runs out of memory, often because the base case is never reached'),
           ('unwinding', 'the process of recursive calls returning one by one, combining their results, after the base case is reached')],
    facts=[('What happens if a recursive function has no reachable base case?', 'It calls itself until the call stack overflows', ['It returns 0', 'It runs once', 'The compiler converts it to a loop'], 'Each call uses stack space.'),
           ('What is returned by fact(4) where fact(n) = 1 if n ≤ 1 else n × fact(n − 1)?', '24', ['4', '10', '16'], '4 × 3 × 2 × 1.'),
           ('Which problem is naturally solved by recursion?', 'Traversing a folder that contains sub-folders', ['Adding two numbers', 'Reading one line of input', 'Swapping two variables'], 'Each sub-folder is the same problem on a smaller scale.'),
           ('Compared with an equivalent loop, a recursive solution usually…', 'uses more memory because of the call stack', ['uses no memory', 'is always faster', 'cannot return values'], 'Every call stores a stack frame.')],
    why=[('Explain why every recursive function needs a base case.', 'The base case stops the chain of calls; without it (or if it is never reached) the function keeps calling itself until the call stack runs out of memory.'),
         ('Explain why naive recursive Fibonacci is very slow.', 'fib(n) calls fib(n − 1) and fib(n − 2), which recompute the same values many times, so the number of calls grows exponentially (about 2^n); storing results (memoisation) or a loop makes it O(n).'),
         ('Explain why recursion can make some algorithms easier to write.', 'Problems with a self-similar structure (trees, nested folders, divide and conquer) can be expressed directly as "solve a smaller version and combine", giving short, clear code that mirrors the definition.')],
    contrast=[('recursion', 'iteration', 'Recursion solves a problem by a function calling itself on smaller inputs (uses the call stack, natural for self-similar problems); iteration repeats a loop body while a condition holds (usually less memory and faster).'),
              ('the base case', 'the recursive case', 'The base case returns directly without recursion and ends the calls; the recursive case calls the function again with a smaller problem.')],
    misc=[('Recursion is always more efficient than loops.', 'Recursion has function-call and stack overhead; iteration is often faster and uses less memory.'),
          ('The base case is executed first when a recursive function is called.', 'The function first checks the base case condition; if it is not met, the recursive case runs, and the base case is reached only after several calls.'),
          ('A recursive function can only call itself once in its body.', 'It can make several recursive calls (e.g. fib, tree traversal, merge sort).')],
    evaluate=[('Programmers should replace all recursion with loops.', ['loops avoid stack overflow and call overhead'], ['recursive code is clearer for trees and divide-and-conquer', 'some languages optimise tail recursion', 'converting may need an explicit stack, making code harder to read'], 'Use recursion where it expresses the problem clearly and depth is bounded; use loops for simple repetition or very deep processing.')],
    extended=[('Write a recursive Python function power(b, e) that calculates b^e for a non-negative integer e, trace power(2, 5) showing the calls and returns, and explain how the function could be made more efficient by using e // 2.', 'def power(b, e): if e == 0: return 1; return b * power(b, e − 1). Calls power(2,5) → power(2,4) → … → power(2,0) returns 1; returns 2, 4, 8, 16, 32. Faster: half = power(b, e // 2); return half*half if e even else b*half*half – O(log e) calls instead of O(e).', 6)],
))


def _rec_case(rng):
    kind = rng.choice(['sumdigits', 'fact', 'fib', 'pow', 'count', 'rev', 'mystery'])
    a = rng.randint(3, 7)
    if kind == 'sumdigits':
        n = rng.randint(100, 9999)
        return f'def f(n):\n    if n < 10:\n        return n\n    return n % 10 + f(n // 10)\n\nprint(f({n}))', 'f'
    if kind == 'fact':
        return f'def f(n):\n    if n <= 1:\n        return 1\n    return n * f(n - 1)\n\nprint(f({a}))', 'f'
    if kind == 'fib':
        return f'def f(n):\n    if n < 2:\n        return n\n    return f(n - 1) + f(n - 2)\n\nprint(f({a + 1}))', 'f'
    if kind == 'pow':
        return f'def f(b, e):\n    if e == 0:\n        return 1\n    return b * f(b, e - 1)\n\nprint(f({rng.randint(2, 3)}, {a}))', 'f'
    if kind == 'count':
        return f'def f(n):\n    if n == 0:\n        return\n    print(n, end=" ")\n    f(n - 1)\n    print(n, end=" ")\n\nf({min(a, 4)})', 'f'
    if kind == 'rev':
        w = rng.choice(['CODE', 'BYTES', 'GRAPH', 'TREE'])
        return f'def f(s):\n    if s == "":\n        return ""\n    return f(s[1:]) + s[0]\n\nprint(f("{w}"))', 'f'
    return f'def f(n):\n    if n <= 0:\n        return 0\n    return n + f(n - 2)\n\nprint(f({rng.randint(5, 11)}))', 'f'


def _count_calls(code):
    src = code.replace('def f(', 'def f(*_a, **_k):\n    global CALLS\n    CALLS += 1\n    return _f(*_a, **_k)\n\ndef _f(', 1)
    src = src.split('\n')
    # recursive calls inside _f should go through f (counter) – they already call f
    g = {'CALLS': 0}
    import contextlib as _cl, io as _i
    with _cl.redirect_stdout(_i.StringIO()):
        exec('CALLS = 0\n' + '\n'.join(src), g)
    return g['CALLS']


@R.add('ch11-st4', 'C3', (2, 5), 'short')
def rec_out(rng, slot):
    code, _ = _rec_case(rng)
    out = run_py(code).strip()
    calls = _count_calls(code)
    stem = rng.choice(_FRAMES).format(code=code, who=rng.choice(PEOPLE))
    ans = out
    key = f'Output: {out}.'
    m = 2
    if slot.d >= 4:
        stem += '\nAlso state how many times f is called in total, and identify the base case.'
        ans += f'; f is called {calls} times'
        key += f' f is called {calls} times (1); base case identified as the branch that returns without calling f (1).'
        m = 4
    return dict(stem=stem, answer=ans, markingKey=key, marks=m)


@R.add('ch11-st4', 'C3', (3, 5), 'short')
def rec_bug(rng, slot):
    items = [('def countdown(n):\n    print(n)\n    countdown(n - 1)', 'There is no base case, so it recurses until RecursionError (stack overflow).', 'add "if n == 0: return" (or if n < 0) before the recursive call'),
             ('def total(n):\n    if n == 0:\n        return 0\n    return n + total(n)', 'The argument is not reduced, so the base case is never reached – infinite recursion / RecursionError.', 'call total(n - 1)'),
             ('def fact(n):\n    if n == 1:\n        return 1\n    return n * fact(n - 1)\n\nprint(fact(0))', 'fact(0) skips the base case (n == 1) and recurses through −1, −2, … – RecursionError.', 'use "if n <= 1: return 1"'),
             ('def length(s):\n    if s == "":\n        return 1\n    return 1 + length(s[1:])', 'Logic error: the base case returns 1 instead of 0, so every length is one too large.', 'return 0 in the base case')]
    code, why, fix = rng.choice(items)
    return dict(stem=f'The recursive function below does not work as intended. Explain the problem and correct it.\n{code}', answer=f'{why} Fix: {fix}.',
                markingKey=f'Problem identified: {why} (2); correction: {fix} (1).', type='explain', marks=3)


K.ar('ch11-st4', [
    ('Recursive functions need a base case.', 'Without a base case, the function would keep calling itself.', 0, 'Both true; R explains A.'),
    ('Recursion uses less memory than iteration.', 'Each recursive call creates a new stack frame.', 3, 'A false; R true and explains why recursion uses more memory.'),
    ('Naive recursive Fibonacci is inefficient.', 'It recalculates the same values many times.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch11-st4', [
    ('Write a recursive Python function sum_list(lst) that returns the sum of a list of numbers without using loops or sum().',
     'def sum_list(lst):\n    if not lst:\n        return 0\n    return lst[0] + sum_list(lst[1:])',
     'assert sum_list([4, 7, 1]) == 12\nassert sum_list([]) == 0', 3),
    ('Write a recursive Python function binary_string(n) that returns the binary representation of a non-negative integer n as a string, e.g. binary_string(13) returns "1101".',
     'def binary_string(n):\n    if n < 2:\n        return str(n)\n    return binary_string(n // 2) + str(n % 2)',
     'assert binary_string(13) == "1101"\nassert binary_string(0) == "0"\nassert binary_string(8) == "1000"', 4),
    ('Write a recursive Python function count_occ(s, ch) that returns how many times the character ch occurs in the string s.',
     'def count_occ(s, ch):\n    if s == "":\n        return 0\n    return (1 if s[0] == ch else 0) + count_occ(s[1:], ch)',
     'assert count_occ("banana", "a") == 3\nassert count_occ("", "x") == 0', 4),
], d=(3, 5))


R.facts('ch11-st5', F(
    terms=[('empirical analysis', 'measuring an algorithm\'s actual running time (or operation count) on inputs of different sizes to estimate its efficiency'),
           ('benchmark', 'a standard test used to measure and compare the performance of programs or hardware'),
           ('doubling experiment', 'measuring running time as the input size doubles; the ratio of times indicates the growth rate (about 2 for O(n), 4 for O(n²))'),
           ('operation count', 'the number of key operations, such as comparisons or swaps, an algorithm performs on a given input'),
           ('profiling', 'measuring which parts of a program use the most time or memory, using a profiler tool')],
    facts=[('In a doubling experiment, times increase by a factor of about 4 each time n doubles. The algorithm is probably…', 'O(n²)', ['O(n)', 'O(log n)', 'O(n³)'], '2² = 4.'),
           ('Why are timings usually repeated several times and averaged?', 'Other processes, caching and the OS cause random variation', ['The first run is always wrong', 'Computers slow down over time', 'It makes the algorithm faster'], 'Averaging reduces noise.'),
           ('Counting comparisons rather than measuring seconds has the advantage that…', 'the result does not depend on the hardware', ['it is always smaller', 'it includes network delays', 'it measures memory use'], 'Operation counts are machine-independent.'),
           ('If doubling n multiplies the time by about 8, the growth rate is about…', 'O(n³)', ['O(n²)', 'O(2n)', 'O(n log n)'], '2³ = 8.')],
    why=[('Explain why empirical timing results may differ between two computers running the same algorithm.', 'Processor speed, cache sizes, memory, the OS, background processes and the language implementation all change the actual time, even though the growth rate (Big O) is the same.'),
         ('Explain why small input sizes are not useful for estimating Big O empirically.', 'For small n, fixed overheads and constant factors dominate and timer resolution is coarse, so the growth pattern only becomes visible for larger inputs.'),
         ('Explain why testing on different kinds of input (random, sorted, reversed) matters.', 'Many algorithms have different best, average and worst cases (e.g. bubble sort with early exit is O(n) on sorted data), so testing several input types reveals the full performance picture.')],
    contrast=[('theoretical analysis (Big O)', 'empirical analysis', 'Theoretical analysis predicts growth from the algorithm\'s structure, independent of hardware; empirical analysis measures real times or counts on actual inputs, which includes constants and system effects.')],
    misc=[('If one run of algorithm A is faster than one run of algorithm B, A is always more efficient.', 'One measurement on one input size says little; growth rate across sizes and repeated runs is needed.'),
          ('Empirical tests prove the exact Big O of an algorithm.', 'They suggest the growth rate for the tested inputs; proof requires analysing the algorithm.'),
          ('Timing results are unaffected by other programs running.', 'Background processes compete for the CPU and cache, adding variation.')],
    evaluate=[('Empirical testing is more useful than Big O analysis for choosing an algorithm.', ['captures real constants, hardware and data effects'], ['results depend on the machine and inputs tested', 'cannot easily predict behaviour for much larger inputs', 'Big O explains why performance scales'], 'Both are needed: Big O to predict scaling, empirical tests to confirm performance on realistic data and hardware.')],
    extended=[('Design an experiment to compare the efficiency of bubble sort and Python\'s built-in sorted() on lists of 1000, 2000, 4000 and 8000 random integers. Describe how you would ensure fair, reliable results and how you would interpret the ratios.', 'Generate the same random lists for both (fixed seed); time with time.perf_counter over several repeats and take the median/mean; exclude list generation from timing; also test sorted and reversed inputs. Compute T(2n)/T(n): ≈4 for bubble sort (O(n²)), ≈2.1-2.2 for sorted() (O(n log n)). Plot time vs n. Keep other programs closed.', 6)],
))


@R.add('ch11-st5', 'C3', (2, 5), 'short')
def doubling(rng, slot):
    bo, fac = rng.choice([('O(n)', 2), ('O(n²)', 4), ('O(n³)', 8), ('O(n log n)', None), ('O(log n)', None)])
    base = rng.choice([0.012, 0.05, 0.2, 0.8, 1.5])
    ns = [1000, 2000, 4000, 8000]
    ts = []
    for k, n in enumerate(ns):
        if bo == 'O(n log n)':
            t = base * (n * math.log2(n)) / (1000 * math.log2(1000))
        elif bo == 'O(log n)':
            t = base * math.log2(n) / math.log2(1000)
        else:
            t = base * fac ** k
        ts.append(t * (1 + rng.uniform(-0.03, 0.03)))
    ts = [float(f'{t:.3g}') for t in ts]
    rows = ', '.join(f'n = {n}: {t:g} s' for n, t in zip(ns, ts))
    ratios = [ts[i + 1] / ts[i] for i in range(3)]
    nxt = 16000
    pred = ts[-1] * (fac if fac else (nxt * math.log2(nxt)) / (8000 * math.log2(8000)) if bo == 'O(n log n)' else math.log2(nxt) / math.log2(8000))
    return dict(stem=f'An algorithm was timed on inputs of different sizes: {rows}. Calculate the ratios of successive times, use them to suggest the time complexity, and predict the time for n = {nxt}.',
                answer=f'Ratios ≈ {", ".join(r2(x, 2) for x in ratios)}; suggests {bo}; predicted ≈ {pred:.3g} s',
                markingKey=f'Ratios {", ".join(r2(x, 2) for x in ratios)} (1); interpretation: ×2 → O(n), ×4 → O(n²), ×8 → O(n³), slightly above ×2 → O(n log n), small constant increase → O(log n): {bo} (2); prediction ≈ {pred:.3g} s (1).', marks=4)


@R.add('ch11-st5', 'C3', (2, 5), 'short')
def op_count(rng, slot):
    n = rng.choice([4, 6, 8, 10])
    kind = rng.choice(['sorted', 'reversed', 'random'])
    if kind == 'sorted':
        arr = list(range(1, n + 1))
    elif kind == 'reversed':
        arr = list(range(n, 0, -1))
    else:
        arr = rng.sample(range(1, 50), n)
    passes, comps, swaps = _bubble_passes(arr)
    return dict(stem=f'Bubble sort with an early-exit flag is run on the {kind} list {arr}. Count the number of comparisons and swaps it performs, and explain what this suggests about its best and worst cases.',
                answer=f'{comps} comparisons, {swaps} swaps ({len(passes)} passes)', markingKey=f'{comps} comparisons (1), {swaps} swaps (1); sorted input → one pass of n − 1 = {n - 1} comparisons (best case O(n)); reversed → n(n − 1)/2 = {n * (n - 1) // 2} comparisons and swaps (worst case O(n²)) (1-2).', marks=4)


K.ar('ch11-st5', [
    ('Timing an algorithm on several input sizes can reveal its growth rate.', 'The ratio of times as n doubles depends on the algorithm\'s complexity.', 0, 'Both true; R explains A.'),
    ('Empirical timings are identical on every computer.', 'Big O ignores hardware differences.', 3, 'A false; R true.'),
    ('Repeating timing runs improves reliability.', 'Background activity causes random variation in timings.', 0, 'Both true; R explains A.'),
])


# =============================================================================================
# ch12 B2.5 File processing
# =============================================================================================
def file_item(rng, files, code, marks=3, intro=None):
    store = dict(files)
    out = '\n'.join(l.rstrip() for l in run_py(code, store).split('\n'))
    shown = '\n'.join(f'File {n} contains:\n{t.rstrip(chr(10))}' for n, t in files.items())
    stem = (intro or rng.choice(['Consider the file(s) and Python program below.', 'A program processes a text file.', 'The following file is stored in the program\'s folder.'])) + \
        f'\n{shown}\nProgram:\n{code}\nState the exact output.'
    return dict(stem=stem, answer=out.replace('\n', ' / ') if out else '(no output)', type='short', marks=marks,
                markingKey=f'Output (lines separated by /): {out.replace(chr(10), " / ") if out else "(none)"}. Award marks for correctly reading/processing each line (strip newlines, convert types) and for the exact final output.'), store


def _people_file(rng, k):
    names = rng.sample(PEOPLE, k)
    return names, [rng.randint(35, 99) for _ in names]


R.facts('ch12-st1', F(
    terms=[('text file', 'a file that stores data as a sequence of characters organised into lines, readable by humans'),
           ('file mode', 'the argument to open() that sets how a file is used: "r" read, "w" write (overwrite), "a" append'),
           ('file handle', 'the object returned by open() through which a program reads from or writes to a file'),
           ('end of file (EOF)', 'the point at which there is no more data to read from a file'),
           ('newline character', 'the special character \\n that marks the end of a line in a text file'),
           ('context manager (with statement)', 'a Python construct that opens a file and guarantees it is closed automatically when the block ends, even if an error occurs')],
    facts=[('Which Python method reads all lines of a file into a list?', 'readlines()', ['readline()', 'read(1)', 'write()'], 'Each list item is one line including its newline.'),
           ('Why is line.strip() often used when reading a text file?', 'To remove the newline character and surrounding spaces', ['To convert text to numbers', 'To close the file', 'To sort the lines'], 'Each line read ends with \\n.'),
           ('What happens if a program opens a non-existent file in "r" mode?', 'A FileNotFoundError is raised', ['An empty file is created', 'The program reads blank lines', 'Python creates a backup'], 'Reading requires the file to exist.'),
           ('In Java, which class is commonly used to read a text file line by line?', 'BufferedReader (with FileReader)', ['PrintWriter', 'ArrayList', 'Math'], 'readLine() returns null at EOF.')],
    why=[('Explain why a file should be closed after it has been used.', 'Closing flushes any buffered data to storage, releases the operating-system resources (file handle/lock) so other programs can use the file, and avoids data loss or corruption if the program ends unexpectedly.'),
         ('Explain why "with open(...) as f:" is preferred to calling open() and close() separately.', 'The with statement automatically closes the file when the block finishes, even if an exception occurs, so files are never left open by mistake.'),
         ('Explain why numbers read from a text file must be converted before calculations.', 'Everything in a text file is read as strings; "12" + "5" concatenates to "125", so int() or float() is needed to treat values as numbers.')],
    contrast=[('read()', 'readline()', 'read() returns the whole remaining file as one string; readline() returns only the next line (including its newline), or "" at the end of the file.'),
              ('a text file', 'a binary file', 'A text file stores characters in lines and is human-readable; a binary file stores raw bytes (images, executables) that must be interpreted by a program.')],
    misc=[('Reading a file deletes its contents.', 'Reading does not change the file; opening in "w" mode is what erases existing contents.'),
          ('readline() returns the line without the newline character.', 'readline() keeps the trailing \\n; strip() or rstrip("\\n") removes it.'),
          ('A for loop over a file handle reads only the first line.', 'Iterating over a file handle yields every line in turn until end of file.')],
    evaluate=[('Text files are an adequate way to store data for a small business application.', ['simple, human-readable, no extra software', 'easy to back up and transfer (CSV)'], ['no enforced structure or validation', 'slow searching and updating of large files', 'no multi-user access control or concurrency'], 'Adequate for small, single-user data or exports; a database is better as data grows or is shared.')],
    extended=[('A weather station in Windhoek writes one temperature reading per line to readings.txt. Write a Python program that reads the file, ignores blank or invalid lines, and outputs the number of valid readings, the mean and the maximum, explaining how the file is opened, read and closed safely.', 'with open("readings.txt") as f: for line in f: line = line.strip(); if not line: continue; try: t = float(line) except ValueError: continue; vals.append(t). After the block the file is closed automatically. Output len(vals), round(sum(vals)/len(vals), 1), max(vals); guard against an empty list; handle FileNotFoundError with try/except.', 6)],
))


@R.add('ch12-st1', 'C3', (1, 5), 'short')
def read_file(rng, slot):
    names, marks = _people_file(rng, rng.randint(4, 6))
    fn = rng.choice(['marks.txt', 'scores.txt', 'results.txt'])
    th = rng.choice([50, 60, 70])
    text = ''.join(f'{n},{m}\n' for n, m in zip(names, marks))
    forms = [f'f = open("{fn}", "r")\ncount = 0\nfor line in f:\n    count += 1\nf.close()\nprint(count)',
             f'with open("{fn}") as f:\n    first = f.readline().strip()\n    second = f.readline().strip()\nprint(first.split(",")[0], second.split(",")[1])',
             f'total = 0\nwith open("{fn}") as f:\n    for line in f:\n        name, mark = line.strip().split(",")\n        total += int(mark)\nprint(total)',
             f'with open("{fn}") as f:\n    lines = f.readlines()\nprint(len(lines), lines[-1].strip())',
             f'passed = []\nwith open("{fn}") as f:\n    for line in f:\n        parts = line.strip().split(",")\n        if int(parts[1]) >= {th}:\n            passed.append(parts[0])\nprint(passed)',
             f'with open("{fn}") as f:\n    data = f.read()\nprint(len(data.split()), data.count("{names[0][0]}"))']
    code = rng.choice(forms if slot.d >= 3 else forms[:4])
    return file_item(rng, {fn: text}, code, marks=2 if slot.d <= 2 else 3)[0]


@R.add('ch12-st1', 'C3', (2, 4), 'short')
def file_error(rng, slot):
    fn = rng.choice(['data.txt', 'log.txt', 'stock.txt'])
    exists = rng.random() < 0.5
    code = f'try:\n    with open("{fn}") as f:\n        n = int(f.readline())\n    print("read", n)\nexcept FileNotFoundError:\n    print("missing")\nexcept ValueError:\n    print("bad data")\nfinally:\n    print("done")'
    files = {fn: rng.choice(['42\n', 'abc\n', '7\n8\n'])} if exists else {}
    store = dict(files)
    out = run_py(code, store).replace('\n', ' / ')
    desc = f'The file {fn} contains:\n{files[fn].rstrip()}' if exists else f'The file {fn} does not exist.'
    return dict(stem=f'{desc}\nState the output of this program and explain the role of the finally block.\n{code}', answer=f'{out}; finally always runs (e.g. for clean-up)',
                markingKey=f'Output {out} (2); finally runs whether or not an exception occurred (1).', marks=3)


K.ar('ch12-st1', [
    ('Lines read from a file usually end with a newline character.', 'Text files mark the end of each line with \\n.', 0, 'Both true; R explains A.'),
    ('Opening a file in "r" mode creates it if it does not exist.', 'Read mode is used to read existing data.', 3, 'A false (FileNotFoundError); R true.'),
    ('A with statement closes a file automatically.', 'The file is closed when the with block ends, even after an exception.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch12-st1', [
    ('Write a Python function average_from_file(filename) that reads one number per line from a text file, skips blank lines, and returns the mean rounded to 2 dp (or None if there are no numbers).',
     'def average_from_file(filename):\n    vals = []\n    with open(filename) as f:\n        for line in f:\n            line = line.strip()\n            if line:\n                vals.append(float(line))\n    if not vals:\n        return None\n    return round(sum(vals) / len(vals), 2)',
     'from ib_cs_common import fake_open\nopen = fake_open({"t.txt": "3\\n\\n4.5\\n6\\n", "e.txt": ""})\nassert average_from_file("t.txt") == 4.5\nassert average_from_file("e.txt") is None', 4),
    ('Write a Python function longest_line(filename) that returns the longest line in a text file (without its newline character).',
     'def longest_line(filename):\n    best = ""\n    with open(filename) as f:\n        for line in f:\n            line = line.rstrip("\\n")\n            if len(line) > len(best):\n                best = line\n    return best',
     'from ib_cs_common import fake_open\nopen = fake_open({"p.txt": "ab\\nabcd\\nabc\\n"})\nassert longest_line("p.txt") == "abcd"', 3),
], d=(3, 5))


R.facts('ch12-st2', F(
    terms=[('write mode ("w")', 'a file mode that creates the file if necessary and erases any existing contents before writing'),
           ('append mode ("a")', 'a file mode that adds new data to the end of an existing file without removing what is already there'),
           ('buffer', 'an area of memory where data is held temporarily before being written to storage'),
           ('flush', 'forcing buffered data to be written to the file immediately'),
           ('serialisation', 'converting data structures into a format (e.g. CSV or JSON text) that can be written to a file and read back later')],
    facts=[('A program opens results.txt in "w" mode and writes one line. What happens to the old contents?', 'They are erased and replaced', ['They are kept and the line is added at the end', 'They are kept and the line is added at the start', 'An error occurs'], '"w" truncates the file.'),
           ('Which mode should a program use to add a new entry to the end of a log file?', '"a"', ['"w"', '"r"', '"x"'], 'Append preserves existing data.'),
           ('What does f.write("Score: " + str(7)) write if no newline is added?', 'Score: 7 with no line break after it', ['Score: 7 followed by a new line', 'An error because write needs a list', '"Score: " only'], 'write() does not add \\n automatically.'),
           ('In Java, which class is commonly used with FileWriter to write lines of text?', 'PrintWriter / BufferedWriter', ['Scanner', 'BufferedReader', 'Random'], 'Writers output text; readers input it.')],
    why=[('Explain why a program that logs events should use append mode rather than write mode.', 'Append mode keeps every previous entry and adds the new event at the end; write mode would erase the log each time the program runs, losing the history.'),
         ('Explain why data written to a file may not appear immediately if the program crashes.', 'Output is buffered in memory for efficiency and only written to storage when the buffer fills, is flushed, or the file is closed; a crash before that loses the buffered data.'),
         ('Explain why numbers must be converted to strings before being written with write().', 'write() accepts only strings for text files, so numbers are converted with str() or formatted (f-strings), and separators/newlines must be added explicitly so the data can be read back.')],
    contrast=[('write mode', 'append mode', 'Write mode ("w") erases existing contents (or creates the file) before writing; append mode ("a") keeps existing contents and adds new data at the end.'),
              ('write()', 'writelines()', 'write() writes a single string; writelines() writes every string in a list or iterable, without adding newlines.')],
    misc=[('f.write() automatically starts a new line after each call.', 'write() writes exactly the string given; "\\n" must be included to end a line.'),
          ('Append mode fails if the file does not already exist.', 'Append mode creates the file if it does not exist.'),
          ('Opening a file in "w" mode and closing it without writing leaves the old contents.', 'Opening in "w" mode immediately truncates the file, so it is left empty.')],
    evaluate=[('CSV is the best format for saving a program\'s data.', ['simple, human-readable, opens in spreadsheets', 'easy to read and write with code'], ['no data types – everything is text', 'commas inside values need quoting', 'nested structures need JSON or a database'], 'CSV suits flat tables; JSON or a database is better for structured, typed or nested data.')],
    extended=[('A gym in Santiago records each visit as "member_id,date,minutes" in visits.csv. Write Python code that appends a new visit, then rewrites a summary file summary.txt listing each member\'s total minutes, explaining your choice of file modes.', 'with open("visits.csv", "a") as f: f.write(f"{mid},{date},{mins}\\n") – append keeps history. Then read visits.csv, accumulate totals in a dictionary, and with open("summary.txt", "w") as out: for m, t in sorted(totals.items()): out.write(f"{m}: {t}\\n") – write mode because the summary is regenerated each time.', 6)],
))


@R.add('ch12-st2', 'C3', (1, 5), 'short')
def write_seq(rng, slot):
    fn = rng.choice(['log.txt', 'out.txt', 'notes.txt', 'orders.txt'])
    start = rng.choice(['', 'START\n', 'old line\n'])
    w = rng.sample(['alpha', 'beta', 'gamma', 'delta', 'omega', 'sigma'], 3)
    seqs = [[('a', w[0]), ('a', w[1])], [('w', w[0]), ('a', w[1]), ('a', w[2])], [('a', w[0]), ('w', w[1]), ('a', w[2])], [('w', w[0]), ('w', w[1])],
            [('a', w[0]), ('a', w[1]), ('w', w[2]), ('a', w[0])]]
    seq = rng.choice(seqs if slot.d >= 3 else seqs[:2])
    body = '\n'.join(f'with open("{fn}", "{m}") as f:\n    f.write("{t}\\n")' for m, t in seq)
    code = body + f'\nwith open("{fn}") as f:\n    print(f.read().split())'
    files = {fn: start} if start else {}
    intro = (f'The file {fn} initially contains the single line "{start.strip()}".' if start else f'The file {fn} does not exist yet.') + ' Consider this program.'
    store = dict(files)
    out = run_py(code, store)
    return dict(stem=f'{intro}\n{code}\nState the exact output and explain the effect of each file mode used.', answer=out,
                markingKey=f'Output {out} (2); ' + ('"w" erases the existing contents before writing' if any(m == 'w' for m, _ in seq) else '') + ('; ' if len({m for m, _ in seq}) > 1 else '') + ('"a" adds to the end of the file (creating it if missing)' if any(m == 'a' for m, _ in seq) else '') + ' (1-2).', marks=3 if slot.d <= 3 else 4)


@R.add('ch12-st2', 'C3', (2, 5), 'short')
def write_records(rng, slot):
    names, marks = _people_file(rng, 4)
    th = rng.choice([50, 60, 70])
    code = (f'data = {list(zip(names, marks))}\nwith open("pass.txt", "w") as f:\n    for name, mark in data:\n        if mark >= {th}:\n            f.write(name + "," + str(mark) + "\\n")\n'
            f'with open("pass.txt") as f:\n    lines = f.readlines()\nprint(len(lines))\nprint(lines[0].strip() if lines else "empty")')
    store = {}
    out = run_py(code, store)
    return dict(stem=f'State the output of this program and the final contents of pass.txt.\n{code}', answer=f'Output: {out.replace(chr(10), " / ")}; pass.txt: {store["pass.txt"].strip().replace(chr(10), " | ") or "(empty)"}',
                markingKey=f'Output {out.replace(chr(10), " / ")} (2); file contents {store["pass.txt"].strip().replace(chr(10), " | ") or "(empty)"} (1).', marks=3)


K.ar('ch12-st2', [
    ('Opening a file in "w" mode erases its existing contents.', 'Write mode truncates the file before writing.', 0, 'Both true; R explains A.'),
    ('write() adds a newline after the text automatically.', 'print() adds a newline by default.', 3, 'A false; R true (print, not write, adds \\n).'),
    ('Append mode is suitable for log files.', 'Append mode adds data to the end without removing existing entries.', 0, 'Both true; R explains A.'),
])

K.code_tasks('ch12-st2', [
    ('Write a Python function save_scores(filename, scores) that writes a dictionary of name → score to a CSV file, one "name,score" per line in alphabetical order of name, replacing any previous contents.',
     'def save_scores(filename, scores):\n    with open(filename, "w") as f:\n        for name in sorted(scores):\n            f.write(f"{name},{scores[name]}\\n")',
     'from ib_cs_common import fake_open\nst = {"s.csv": "old\\n"}\nopen = fake_open(st)\nsave_scores("s.csv", {"Omar": 7, "Ana": 9})\nassert st["s.csv"] == "Ana,9\\nOmar,7\\n"', 4),
    ('Write a Python function log_event(filename, message) that appends a line "#n message" to a log file, where n is one more than the number of lines already in the file (the file may not exist yet).',
     'def log_event(filename, message):\n    try:\n        with open(filename) as f:\n            n = len(f.readlines())\n    except FileNotFoundError:\n        n = 0\n    with open(filename, "a") as f:\n        f.write(f"#{n + 1} {message}\\n")',
     'from ib_cs_common import fake_open\nst = {}\nopen = fake_open(st)\nlog_event("l.txt", "start")\nlog_event("l.txt", "stop")\nassert st["l.txt"] == "#1 start\\n#2 stop\\n"', 5),
], d=(3, 5))


R.facts('ch12-st3', F(
    terms=[('record', 'a collection of related fields describing one item, such as one line of a CSV file'),
           ('field', 'one item of data within a record, such as a name or a score'),
           ('delimiter', 'a character such as a comma or tab that separates fields within a line of a file'),
           ('CSV file', 'a text file storing tabular data with one record per line and fields separated by commas'),
           ('parsing', 'analysing a line of text and splitting it into its component fields, converting each to the correct data type'),
           ('header row', 'the first line of a CSV file, which names the fields rather than holding data')],
    facts=[('Which Python method splits "Lima,Peru,9.7" into ["Lima", "Peru", "9.7"]?', 'split(",")', ['strip(",")', 'join(",")', 'replace(",")'], 'split separates on the delimiter.'),
           ('When loading a CSV file with a header row, what must the program do?', 'Skip or use the first line rather than treating it as data', ['Delete the file', 'Sort the header', 'Convert the header to numbers'], 'Otherwise int("score") raises ValueError.'),
           ('Which structure is most convenient for looking up a product\'s price by its code after loading a file?', 'A dictionary keyed by code', ['A stack', 'A queue', 'A single string'], 'Direct lookup by key.'),
           ('A record "Ana,17,Geneva" is split by commas. What is fields[1]?', '"17" (a string)', ['17 (an integer)', '"Ana"', '"Geneva"'], 'Indices start at 0 and split returns strings.')],
    why=[('Explain why data from a file is often loaded into a list or dictionary before processing.', 'Once in memory the records can be searched, sorted, filtered and updated quickly and repeatedly without re-reading the slow file, and fields are converted to the correct types once.'),
         ('Explain why a field containing a comma can break a simple CSV parser.', 'split(",") treats every comma as a delimiter, so "Smith, J" becomes two fields and the rest of the record shifts; proper CSV uses quotes and a csv module that understands them.'),
         ('Explain why each record should be validated as it is loaded.', 'Files may contain blank lines, missing fields or invalid values; checking (and skipping or reporting) bad records prevents run-time errors and incorrect results later.')],
    contrast=[('a list of lists', 'a list of dictionaries', 'In a list of lists each record\'s fields are accessed by position (row[1]); in a list of dictionaries they are accessed by name (row["score"]), which is clearer and robust to column order.'),
              ('a record', 'a field', 'A record is all the data about one item (one line); a field is a single attribute within it.')],
    misc=[('After line.split(","), numeric fields can be added directly.', 'split returns strings; they must be converted with int() or float() first.'),
          ('The header row of a CSV file is ignored automatically by split().', 'split processes every line equally; the program must skip the header (e.g. next(f) or readline()).'),
          ('Loading a whole file into memory is always the best approach.', 'Very large files may not fit in memory; they can be processed line by line.')],
    evaluate=[('Using Python\'s csv module is better than writing your own split-based parser.', ['handles quoted fields, embedded commas and newlines correctly', 'less code and fewer bugs'], ['split is simpler for clean, controlled data', 'learning parsing logic is educational'], 'For real-world CSV the csv module is more reliable; a simple split suffices only for data you control.')],
    extended=[('A city bike-share scheme in Copenhagen exports trips.csv with the header "trip_id,station,minutes". Write a Python program that loads the records into a dictionary of station → list of trip durations, then outputs each station\'s number of trips and average duration, and explain how you would handle malformed lines.', 'with open("trips.csv") as f: next(f); for line in f: parts = line.strip().split(","); if len(parts) != 3: continue; try: m = int(parts[2]) except ValueError: continue; stations.setdefault(parts[1], []).append(m). Then for s, ms in sorted(stations.items()): print(s, len(ms), round(sum(ms)/len(ms), 1)). Malformed lines are skipped (or logged) using length checks and try/except.', 6)],
))


@R.add('ch12-st3', 'C3', (2, 5), 'short')
def csv_records(rng, slot):
    cities = rng.sample(['Lima', 'Oslo', 'Accra', 'Hanoi', 'Quito', 'Seoul', 'Doha', 'Perth'], 3)
    rows = [(f'T{100 + i}', rng.choice(cities), rng.randint(5, 60)) for i in range(rng.randint(5, 7))]
    text = 'trip_id,station,minutes\n' + ''.join(f'{a},{b},{c}\n' for a, b, c in rows)
    forms = [
        'totals = {}\nwith open("trips.csv") as f:\n    f.readline()\n    for line in f:\n        tid, st, mins = line.strip().split(",")\n        totals[st] = totals.get(st, 0) + int(mins)\nfor st in sorted(totals):\n    print(st, totals[st])',
        'trips = []\nwith open("trips.csv") as f:\n    next(f)\n    for line in f:\n        parts = line.strip().split(",")\n        trips.append([parts[0], parts[1], int(parts[2])])\nlongest = max(trips, key=lambda t: t[2])\nprint(len(trips), longest[0], longest[2])',
        f'count = 0\nwith open("trips.csv") as f:\n    header = f.readline().strip().split(",")\n    for line in f:\n        rec = dict(zip(header, line.strip().split(",")))\n        if rec["station"] == "{cities[0]}" and int(rec["minutes"]) > 20:\n            count += 1\nprint(header[2], count)',
        'by = {}\nwith open("trips.csv") as f:\n    f.readline()\n    for line in f:\n        tid, st, mins = line.strip().split(",")\n        by.setdefault(st, []).append(int(mins))\nfor st in sorted(by):\n    print(st, len(by[st]), round(sum(by[st]) / len(by[st]), 1))']
    if len({r[2] for r in rows}) != len(rows):
        return None
    return file_item(rng, {'trips.csv': text}, rng.choice(forms), marks=3 if slot.d <= 3 else 4)[0]


@R.add('ch12-st3', 'C3', (2, 5), 'short')
def bad_records(rng, slot):
    good = [(rng.choice(PEOPLE), rng.randint(30, 99)) for _ in range(4)]
    bad = rng.sample(['', 'Nia', 'Omar,eighty', 'Lars,71,extra', ',55'], 2)
    lines = [f'{n},{m}' for n, m in good] + bad
    rng.shuffle(lines)
    text = '\n'.join(lines) + '\n'
    code = ('valid, errors = [], 0\nwith open("marks.csv") as f:\n    for line in f:\n        parts = line.strip().split(",")\n        if len(parts) != 2 or parts[0] == "":\n            errors += 1\n            continue\n        try:\n            valid.append((parts[0], int(parts[1])))\n        except ValueError:\n            errors += 1\nprint(len(valid), errors)\nprint(sum(m for n, m in valid))')
    return file_item(rng, {'marks.csv': text}, code, marks=4, intro='A program loads records from a file that contains some malformed lines.')[0]


K.ar('ch12-st3', [
    ('Fields split from a CSV line are strings.', 'split() always returns a list of strings.', 0, 'Both true; R explains A.'),
    ('A dictionary is suitable for storing records keyed by a unique ID.', 'Dictionary keys must be unique.', 0, 'Both true; R explains why a unique ID suits a key.'),
    ('The header row should be added to the numeric totals.', 'The header row contains field names.', 3, 'A false; R true and is why the header must be skipped.'),
])

K.code_tasks('ch12-st3', [
    ('Write a Python function load_prices(filename) that reads a CSV file with a header line "code,name,price" and returns a dictionary mapping each code to a (name, price) tuple, with price as a float.',
     'def load_prices(filename):\n    out = {}\n    with open(filename) as f:\n        f.readline()\n        for line in f:\n            line = line.strip()\n            if not line:\n                continue\n            code, name, price = line.split(",")\n            out[code] = (name, float(price))\n    return out',
     'from ib_cs_common import fake_open\nopen = fake_open({"p.csv": "code,name,price\\nA1,Tea,2.5\\nB2,Rice,1.2\\n\\n"})\nassert load_prices("p.csv") == {"A1": ("Tea", 2.5), "B2": ("Rice", 1.2)}', 5),
    ('Write a Python function top_students(filename, n) that reads lines "name,score" and returns a list of the names of the n highest scorers, highest first (ties broken alphabetically).',
     'def top_students(filename, n):\n    recs = []\n    with open(filename) as f:\n        for line in f:\n            name, score = line.strip().split(",")\n            recs.append((-int(score), name))\n    recs.sort()\n    return [name for s, name in recs[:n]]',
     'from ib_cs_common import fake_open\nopen = fake_open({"s.txt": "Mei,80\\nAna,92\\nLars,80\\nOmar,75\\n"})\nassert top_students("s.txt", 3) == ["Ana", "Lars", "Mei"]', 5),
], d=(3, 5))
