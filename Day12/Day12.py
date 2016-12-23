from collections import defaultdict

DATA_FILENAME = "data.txt"

def resolve_value(char, registers):
    return int(registers[char]) if char.isalpha() else int(char)

for default_c in (0, 1):
    lines = open(DATA_FILENAME).read().split("\n")
    registers = defaultdict(int)
    registers["c"] = default_c
    i = 0

    while i < len(lines):
        commands = lines[i].split(" ")

        if len(commands) == 2:
            command, x = commands

            if command == "inc":
                registers[x] += 1

            elif command == "dec":
                registers[x] -= 1

        elif len(commands) == 3:
            command, x, y = commands

            if command == "cpy":
                registers[y] = resolve_value(x, registers)

            elif command == "jnz":
                if resolve_value(x, registers) != 0:
                    i += resolve_value(y, registers) - 1

        i += 1

    print(registers['a']) #part 1 and 2 answer