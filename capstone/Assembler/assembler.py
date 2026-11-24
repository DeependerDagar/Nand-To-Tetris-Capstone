import sys

# ---------- Tables ----------
# Comp bits (a=0 wale). M wali instructions ke liye M ko A se badal kar a=1 lagate hain.
COMP = {
    "0": "101010", "1": "111111", "-1": "111010",
    "D": "001100", "A": "110000", "!D": "001101", "!A": "110001",
    "-D": "001111", "-A": "110011", "D+1": "011111", "A+1": "110111",
    "D-1": "001110", "A-1": "110010", "D+A": "000010", "D-A": "010011",
    "A-D": "000111", "D&A": "000000", "D|A": "010101",
}
# Ulte order wale forms (jaise M+D) ko normal form me badalne ke liye
ALIASES = {"A+D": "D+A", "A&D": "D&A", "A|D": "D|A",
           "1+D": "D+1", "1+A": "A+1"}

JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
for i in range(16):
    PREDEFINED["R" + str(i)] = i


def clean(line):
    """Comment aur spaces hata do."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def comp_bits(c):
    a = "1" if "M" in c else "0"
    c = c.replace("M", "A")
    c = ALIASES.get(c, c)
    return a + COMP[c]


# ---------- Pass 1: labels ----------
def first_pass(raw_lines):
    symbols = dict(PREDEFINED)
    instructions = []      # sirf asli instructions
    seen_labels = set()
    rom = 0                # ROM address counter

    for n, line in enumerate(raw_lines, 1):
        s = clean(line)
        if not s:
            continue
        if s.startswith("("):
            label = s[1:-1]
            if label in seen_labels:
                # K mod 3 = 2 wala feature: warning, crash nahi
                print(f"Warning: Line {n}: label '{label}' is defined more than once")
            else:
                seen_labels.add(label)
                symbols[label] = rom
        else:
            instructions.append(s)
            rom += 1
    return symbols, instructions


# ---------- Pass 2: translate ----------
def second_pass(instructions, symbols):
    out = []
    next_var = 16          # naye variables 16 se shuru
    for s in instructions:
        if s.startswith("@"):                       # A-instruction
            sym = s[1:]
            if sym.isdigit():
                val = int(sym)
            else:
                if sym not in symbols:
                    symbols[sym] = next_var
                    next_var += 1
                val = symbols[sym]
            out.append(format(val, "016b"))
        else:                                       # C-instruction
            dest, jump = "", ""
            if "=" in s:
                dest, s = s.split("=")
            if ";" in s:
                s, jump = s.split(";")
            d = ("1" if "A" in dest else "0") + \
                ("1" if "D" in dest else "0") + \
                ("1" if "M" in dest else "0")
            out.append("111" + comp_bits(s) + d + JUMP[jump])
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py File.asm")
        sys.exit(1)
    src = sys.argv[1]
    with open(src) as f:
        raw = f.readlines()

    symbols, instructions = first_pass(raw)
    result = second_pass(instructions, symbols)

    dst = src.rsplit(".", 1)[0] + ".hack"
    with open(dst, "w") as f:
        f.write("\n".join(result) + "\n")
    print("Written", dst)


if __name__ == "__main__":
    main()