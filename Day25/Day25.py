from collections import defaultdict
from itertools import count

DATA_FILENAME = "data.txt"

def resolve_value(char, registers):
    return int(registers[char]) if char.isalpha() else int(char)

def toggle_line(line):
    swaps = {"tgl":"inc", "dec":"inc", "inc":"dec", "cpy":"jnz", "jnz":"cpy"}
    split_line = line.split(" ")
    split_line[0] = swaps[split_line[0]]
    return ' '.join(split_line)

found = False

for default_a in count(1):
    lines = open(DATA_FILENAME).read().split("\n")
    registers = defaultdict(int)

    registers['a'] = default_a
    i = 0
    clock = []
    while i < len(lines):
        commands = lines[i].split(" ")

        if len(commands) == 1:
            command = commands

            if command == "nop":
                pass

        elif len(commands) == 2:
            command, x = commands

            if command == "inc":
                registers[x] += 1

            elif command == "dec":
                registers[x] -= 1

            elif command == "tgl":
                target_index = i + resolve_value(x, registers)
                if 0 <= target_index < len(lines):
                    lines[target_index] = toggle_line(lines[target_index])

            elif command == "out":
                clock.append(resolve_value(x, registers))
                if len(clock) == 1:
                    if clock[0] != 0:
                        break
                else:
                    if clock[-1] != 1 - clock[-2]:
                        break
                    if len(clock) == 10: #good enough
                        print(default_a)
                        found = True
                        break


        elif len(commands) == 3:
            command, x, y = commands

            if command == "cpy":
                registers[y] = resolve_value(x, registers)

            elif command == "jnz":
                if resolve_value(x, registers) != 0:
                    i += resolve_value(y, registers) - 1


        elif len(commands) == 4:
            command, x, y, z = commands

            if command == "mul":
                x, y = resolve_value(x, registers), resolve_value(y, registers)
                registers[z] = x * y

        i += 1

    if found:
        break