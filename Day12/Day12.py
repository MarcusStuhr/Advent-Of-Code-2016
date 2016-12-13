from collections import defaultdict

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

for defaultC in (0, 1):
    registers = defaultdict(int)
    registers["c"] = defaultC
    i = 0
    while i < len(lines):
        commands = lines[i].split(" ")
        if len(commands) == 2:
            direction, x = commands
            if direction == "inc":
                registers[x] += 1
            else:
                registers[x] -= 1
        elif len(commands) == 3:
            if commands[0] == "cpy":
                cpy, x, y = commands
                if (x.isalpha()):
                    registers[y] = int(registers[x])
                else:
                    registers[y] = int(x)
            else:
                jnz, x, y = commands
                if (not x.isalpha() and x != 0) or (x.isalpha() and registers[x] != 0):
                    if y.isalpha():
                        i += registers[y]
                    else:
                        i += int(y)
                    i -= 1
        i += 1
    print(registers['a']) #part 1 and 2 answer