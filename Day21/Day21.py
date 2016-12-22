from Scrambler import scrambler

instructions = open("data.txt").read().split("\n")
print(scrambler("abcdefgh", instructions)) #part 1 answer
print(scrambler("fbgdceah", instructions, True)) #part 2 answer