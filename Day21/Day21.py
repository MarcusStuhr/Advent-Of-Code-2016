import re
from itertools import permutations

def rotate(code, steps, towards_right = True):
    slice_sign = -1 if towards_right else 1
    steps %= len(code)
    return code[slice_sign * steps:] + code[:slice_sign * steps]

def scrambler(input_string, instructions):
    code = list(input_string)

    for line in instructions:
        nums = re.findall(r"([\d]+)", line)
        letters = re.findall(r"letter ([\w])", line)

        if line.startswith("swap"):
            if len(letters) > 0:
                pos1, pos2 = code.index(letters[0]), code.index(letters[1])
            else:
                pos1, pos2 = map(int, nums)
            code[pos1], code[pos2] = code[pos2], code[pos1]

        elif line.startswith("rotate left"):
            code = rotate(code, int(nums[0]), False)

        elif line.startswith("rotate right"):
            code = rotate(code, int(nums[0]), True)

        elif line.startswith("rotate based"):
            pos = code.index(letters[0])
            if pos >= 4:
                pos += 1
            code = rotate(code, pos + 1, True)

        elif line.startswith("move"):
            from_pos, to_pos = map(int, nums)
            letter_to_insert = code[from_pos]
            code.remove(letter_to_insert)
            code.insert(to_pos, letter_to_insert)

        elif line.startswith("reverse"):
            start_pos, end_pos = map(int, nums)
            code = code[:start_pos] + code[start_pos:end_pos + 1][::-1] + code[end_pos + 1:]

    return ''.join(code)


instructions = open("data.txt").read().split("\n")

print(scrambler("abcdefgh", instructions)) #part 1 answer

for p in permutations("abcdefgh"):
    input_string = ''.join(p)
    if scrambler(input_string, instructions) == "fbgdceah":
        print(input_string) #part 2 answer
        break