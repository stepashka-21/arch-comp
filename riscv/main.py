from sys import argv

inpf = argv[1]
outf = ""
if len(argv) == 3:
    outf = argv[2]

with open(inpf, "rb") as f:
    b = f.read()
pos = 0

l_index = 0

utype = {"0110111": "lui",
         "0010111": "auipc"}

jtype = {"1101111": "jal"}

itype = {"000" + "1100111": "jalr",
         "000" + "0000011": "lb",
         "001" + "0000011": "lh",
         "010" + "0000011": "lw",
         "100" + "0000011": "lbu",
         "101" + "0000011": "lhu",
         "000" + "0010011": "addi",
         "010" + "0010011": "slti",
         "011" + "0010011": "sltiu",
         "100" + "0010011": "xori",
         "110" + "0010011": "ori",
         "111" + "0010011": "andi",
         "001" + "1110011": "csrrw",
         "010" + "1110011": "csrrs",
         "011" + "1110011": "csrrc",
         "101" + "1110011": "csrrwi",
         "110" + "1110011": "csrrsi",
         "111" + "1110011": "csrrci"}

full_len = {"00000000000000000000000001110011": "ecall",
            "00000000000100000000000001110011": "ebreak",
            "00000000000000000001000000001111": "fence.i",
            "00110000001000000000000001110011": "mret",
            "00010000010100000000000001110011": "wfi",
            "00010000001000000000000001110011": "sret",
            "00000000001000000000000001110011": "uret"}

stype = {"000" + "0100011": "sb",
         "001" + "0100011": "sh",
         "010" + "0100011": "sw"}

btype = {"000" + "1100011": "beq",
         "001" + "1100011": "bne",
         "100" + "1100011": "blt",
         "101" + "1100011": "bg",
         "110" + "1100011": "bltu",
         "111" + "1100011": "bgeu"}

rtype = {"0000000" + "001" + "0010011": "slli",
         "0000000" + "101" + "0010011": "srli",
         "0100000" + "101" + "0010011": "srai",
         "0000000" + "000" + "0110011": "add",
         "0100000" + "000" + "0110011": "sub",
         "0000000" + "001" + "0110011": "sll",
         "0000000" + "010" + "0110011": "slt",
         "0000000" + "011" + "0110011": "sltu",
         "0000000" + "100" + "0110011": "xor",
         "0000000" + "101" + "0110011": "srl",
         "0100000" + "101" + "0110011": "sra",
         "0000000" + "110" + "0110011": "or",
         "0000000" + "111" + "0110011": "and",
         # RV32M
         "0000001" + "000" + "0110011": "mul",
         "0000001" + "001" + "0110011": "mulh",
         "0000001" + "010" + "0110011": "mulhsu",
         "0000001" + "011" + "0110011": "mulhu",
         "0000001" + "100" + "0110011": "div",
         "0000001" + "101" + "0110011": "divu",
         "0000001" + "110" + "0110011": "rem",
         "0000001" + "111" + "0110011": "remu"}

ftype = {"0001111": "fence"}

regname = ["zero", "ra", "sp", "gp", "tp"] + ["t0", "t1", "t2", "s0", "s1"] + [f"a{i}" for i in range(8)] + \
          [f"s{i}" for i in range(2, 12)] + [f"t{i}" for i in range(3, 7)]

binds = {0: "LOCAL", 1: "GLOBAL", 2: "WEAK", 10: "LOOS",
         12: "HIOS", 13: "LOPROC", 15: "HIPROC"}

types = {0: "NOTYPE", 1: "OBJECT", 2: "FUNC", 3: "SECTION", 4: "FILE", 5: "COMMON",
         6: "TLS", 7: "UNDEFINED", 8: "UNDEFINED", 9: "UNDEFINED", 10: "LOOS",
         11: "UNDEFINED", 12: "HIOS", 13: "LOPROC", 14: "UNDEFINED", 15: "HIPROC"}

indexes = {0: "UNDEF", 65280: "LOPROC", 65311: "HIPROC", 65312: "LOOS",
           65343: "HIOS", 65521: "ABS", 65522: "COMMON", 65535: "HIRESERVE"} | {i: i for i in range(1, 5000)}

vises = {0: "DEFAULT", 1: "INTERNAL", 2: "HIDDEN", 3: "PROTECTED"}


class ELFHeader:
    entry, phoff, shoff, phentsize, phnum, shentsize, shnum, shstrndx = [0] * 8


class SectionHeader:
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = [0] * 10
    str_name = ""


class Symtab:
    sym_value, sym_size, sym_name, sym_info, sym_other, sym_shndx = [0] * 6


class SymtabEntry:
    st_name, st_value, st_type = [0] * 3
    str_name = ""


def next_bytes(n):
    global pos
    bts = b[pos:pos + n]
    pos += n
    return bts


def next_int(n):
    global pos
    bts = b[pos:pos + n]
    pos += n
    return int.from_bytes(bts, "little")


def skip_b(n):
    global pos
    pos += n


def offset_from_start(offset):
    global pos
    pos = offset


def parse_elf_header():
    header = ELFHeader()
    skip_b(24)
    header.entry = next_int(4)
    header.phoff = next_int(4)
    header.shoff = next_int(4)
    skip_b(6)
    header.phentsize = next_int(2)
    header.phnum = next_int(2)
    header.shentsize = next_int(2)
    header.shnum = next_int(2)
    header.shstrndx = next_int(2)
    return header


def get_str_name(name, strtb):
    global pos
    offset_from_start(strtb.sh_offset + name)
    str_name = ""
    while b[pos] != 0:
        str_name += chr(b[pos])
        pos += 1
    return str_name


def parse_section_header():
    sec = SectionHeader()
    sec.sh_name = next_int(4)
    sec.sh_type = next_int(4)
    sec.sh_flags = next_int(4)
    sec.sh_addr = next_int(4)
    sec.sh_offset = next_int(4)
    sec.sh_size = next_int(4)
    sec.sh_link = next_int(4)
    sec.sh_info = next_int(4)
    sec.sh_addralign = next_int(4)
    sec.sh_entsize = next_int(4)
    return sec


def parse_section_header_table():
    headers = []
    offset_from_start(eh.shoff)
    for _ in range(eh.shnum):
        headers.append(parse_section_header())
    return headers


def get_str_names(lst, strtab):
    for s in lst:
        if isinstance(s, SymtabEntry):
            s.str_name = get_str_name(s.st_name, strtab)

        elif isinstance(s, SectionHeader):
            s.str_name = get_str_name(s.sh_name, strtab)


def find_header(name_x):
    for s in section_headers:
        if s.str_name == name_x:
            return s

    return False


def get_text_section_content():
    offset_from_start(text_header.sh_offset)
    return next_bytes(text_header.sh_size)


def get_symtab_section_content():
    offset_from_start(symtab.sh_offset)
    return next_bytes(symtab.sh_size)


def get_strtab_section_content():
    offset_from_start(strtab.sh_offset)
    return next_bytes(strtab.sh_size)


def parse_entry():
    e = SymtabEntry()
    e.st_name = next_int(4)
    e.st_value = next_int(4)
    skip_b(4)
    e.stype = next_int(1) & 0xf
    skip_b(3)
    return e


def parse_symtab():
    labels = []
    offset_from_start(symtab.sh_offset)
    skip_b(16)
    for i in range(1, symtab.sh_size // 16):
        e = parse_entry()
        if e.st_type != 4:
            labels.append(e)

    return labels


def addr_name():
    d = {}
    for l in labels:
        if l.str_name:
            d[l.st_value] = f"{l.str_name}"
        else:
            d[l.st_value] = f"LOC_{hex8(l.st_value)}"
    return d


def to_signed(s):
    if s[0] == "1":
        return int(s, 2) - (1 << len(s))
    else:
        return int(s, 2)


def hex8(n):
    return hex(n)[2:].zfill(8)


def parse_command(cmd):
    cmd = bin(int.from_bytes(cmd, "little"))[2:].zfill(32)[::-1]
    _6_0 = cmd[0:7][::-1]
    _11_7 = cmd[7:12][::-1]
    _14_12 = cmd[12:15][::-1]
    _19_15 = cmd[15:20][::-1]
    _24_20 = cmd[20:25][::-1]
    _31_25 = cmd[25:32][::-1]
    _31_12 = cmd[12:32][::-1]
    _30_21 = cmd[21:31][::-1]
    _19_12 = cmd[12:20][::-1]
    _27_24 = cmd[24:28][::-1]
    if _6_0 in utype:
        opcode = utype[_6_0]
        rd = regname[int(_11_7, 2)]
        imm = to_signed(_31_12 + "0" * 20)
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rd, imm]
    elif _6_0 in jtype:
        opcode = jtype[_6_0]
        rd = regname[int(_11_7, 2)]
        imm = to_signed(cmd[31] * 12 + _19_12 + cmd[20] + _30_21 + "0")
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rd, imm]
    elif _14_12 + _6_0 in itype:
        opcode = itype[_14_12 + _6_0]
        rd = regname[int(_11_7, 2)]
        rs1 = regname[int(_19_15, 2)]
        imm = to_signed(cmd[31] * 20 + _31_25 + _24_20)
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rd, rs1, imm]
    elif cmd[::-1] in full_len:
        opcode = full_len[cmd[::-1]]
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, ""]
    elif _6_0 in ftype:
        opcode = ftype[_6_0]
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, _27_24, _24_20[1:]]
    elif _14_12 + _6_0 in stype:
        opcode = stype[_14_12 + _6_0]
        rs1 = regname[int(_19_15, 2)]
        rs2 = regname[int(_24_20, 2)]
        imm = to_signed(cmd[31] * 20 + _31_25 + _11_7)
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rs2, rs1, imm]
    elif _14_12 + _6_0 in btype:
        opcode = btype[_14_12 + _6_0]
        rs1 = regname[int(_19_15, 2)]
        rs2 = regname[int(_24_20, 2)]
        imm = to_signed(cmd[31] * 20 + cmd[7] + _31_25 + _11_7[:-1] + "0")
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rs1, imm, rs2]
    elif _31_25 + _14_12 + _6_0 in rtype:
        opcode = rtype[_31_25 + _14_12 + _6_0]
        rd = regname[int(_11_7, 2)]
        rs1 = regname[int(_19_15, 2)]
        rs2 = regname[int(_24_20, 2)]
        he = hex(int(cmd[::-1], 2))[2:]
        res = [opcode, '0' * (8 - len(he)) + he, rd, rs1, rs2]
    else:
        he = hex(int(cmd[::-1], 2))[2:]
        res = ["Unknown command", '0' * (8 - len(he)) + he]
    return res


def disassemble():
    res = []
    for i in range(0, text_header.sh_size, 4):
        command = text[i:i + 4]
        res.append(parse_command(command))
    return res


def parse_sym_tab(tex):
    sp = []
    for i in range(0, len(tex), 16):
        sp.append(int.from_bytes((tex[i:i + 4]), byteorder='little'))
        sp.append(int.from_bytes((tex[i + 4:i + 8]), byteorder='little'))
        sp.append(int.from_bytes((tex[i + 8:i + 12]), byteorder='little'))
        sp.append(int.from_bytes((tex[i + 12:i + 13]), byteorder='little'))
        sp.append(int.from_bytes((tex[i + 13:i + 14]), byteorder='little'))
        sp.append(int.from_bytes((tex[i + 14:i + 16]), byteorder='little'))
    return sp


eh = parse_elf_header()

section_headers = parse_section_header_table()
get_str_names(section_headers, section_headers[eh.shstrndx])

text_header = find_header(".text")
strtab = find_header(".strtab")
symtab = find_header(".symtab")

labels = []
if symtab:
    labels = parse_symtab()
    if strtab:
        get_str_names(labels, strtab)

an = addr_name()

text = get_text_section_content()
symtab_text = get_symtab_section_content()
strtab_text = get_strtab_section_content()

res = disassemble()
sym = Symtab()

st_res = parse_sym_tab(symtab_text)

if outf:
    f = open(outf, "w")
else:
    f = None

addr1 = addr = text_header.sh_addr
for c in res:
    if c[0] in {"beq", "bne", "bltu", "bg", "blt", "bgeu"}:
        if c[3] + addr1 not in an:
            an[c[3] + addr1] = f"L{l_index}"
            l_index += 1
    elif c[0] == "jal":
        if c[3] + addr1 not in an:
            an[c[3] + addr1] = f"L{l_index}"
            l_index += 1
    addr1 += 4

def fen(stro):
    stroka = ""
    if stro[0] == "1":
        stroka += "i"
    if stro[1] == "1":
        stroka += "o"
    if stro[2] == "1":
        stroka += "r"
    if stro[3] == "1":
        stroka += "w"
    return stroka

print(".text\n",file=f)
for c in res:
    if addr in an:
        print("\n%08x \t<%s>:" % (int(hex8(addr), 16), an[addr]), file=f)
    if c[0] in {"sb", "sh", "sw", "lb", "lh", "lw", "lbu", "lhu", "jalr"}:
        print("   %05x:\t%08x\t%7s\t%s, %d(%s)" % (int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[4], c[3]),
              file=f)
    elif c[0] in {"lui", "auipc"}:
        print("   %05x:\t%08x\t%7s\t%s, 0x%x" % (int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[3] // (16 ** 5)),
              file=f)
    elif c[0] in {"beq", "bne", "bltu", "bg", "blt", "bgeu"}:
        print("   %05x:\t%08x\t%7s\t%s, %s, 0x%x, <%s>" % (
            int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[4], c[3] + addr, an[c[3] + addr]),
              file=f)
    elif c[0] == "jal":
        print(
            "   %05x:\t%08x\t%7s\t%s, 0x%x <%s>" % (
            int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[3] + addr, an[c[3] + addr]),
            file=f)
    elif c[0] == "fence":
        print("   %05x:\t%08x\t%7s\t%s, %s" % (int(hex8(addr), 16), int(c[1], 16), c[0], fen(c[2]), fen(c[3])), file=f)
    elif c[0] == "Unknown command":
        print("   %05x:\t%08x\t%-7s" % (int(hex8(addr), 16), int(c[1], 16), c[0]), file=f)
    elif len(c) == 3:
        print("   %05x:\t%08x\t  %-7s" % (int(hex8(addr), 16), int(c[1], 16), c[0]), file=f)
    elif len(c) == 4:
        print("   %05x:\t%08x\t%7s\t%s, %s" % (int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[3]), file=f)
    elif len(c) == 5:
        print("   %05x:\t%08x\t%7s\t%s, %s, %s" % (int(hex8(addr), 16), int(c[1], 16), c[0], c[2], c[3], c[4]),
              file=f)
    addr += 4

def find_name(ind):
    textik = str(strtab_text)[2:]
    textik = textik.replace('\\x00', '#')
    if len(textik) < ind:
        return ""
    textik = textik[ind:].split('#')[0]
    if textik == '#':
        return ""
    else:
        return textik

print("\n\n.symtab\n", file=f)
print("Symbol Value              Size Type     Bind     Vis       Index Name", file=f)
for i in range(len(st_res) // 6):
    print("[%4i] 0x%-15X %5i %-8s %-8s %-8s %6s %s" % (
        i, st_res[i * 6 + 1], st_res[i * 6 + 2], types[st_res[i * 6 + 3] % 16], binds[st_res[i * 6 + 3] // 16],
        vises[(st_res[i * 6 + 4])], indexes[st_res[i * 6 + 5]], find_name(st_res[i * 6])), file=f)

if outf:
    f.close()
