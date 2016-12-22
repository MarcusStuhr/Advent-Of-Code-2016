import re

def rotate(code, steps, towards_right = True):
    slice_sign = -1 if towards_right else 1
    steps %= len(code)
    return code[slice_sign * steps:] + code[:slice_sign * steps]

def scrambler(input_string, instructions, unscramble = False):
    assert len(input_string) % 2 == 0
    code = list(input_string)
    direction = -1 if unscramble else 1

    for line in instructions[::direction]:
        nums = re.findall(r"([\d]+)", line)
        letters = re.findall(r"letter ([\w])", line)

        if line.startswith("swap"):
            if len(letters) > 0:
                pos1, pos2 = code.index(letters[0]), code.index(letters[1])
            else:
                pos1, pos2 = map(int, nums)
            code[pos1], code[pos2] = code[pos2], code[pos1]

        elif line.startswith("rotate left"):
            code = rotate(code, int(nums[0]), False if not unscramble else True)

        elif line.startswith("rotate right"):
            code = rotate(code, int(nums[0]), True if not unscramble else False)

        elif line.startswith("rotate based"):
            pos = code.index(letters[0])
            if (not unscramble):
                steps = pos + 1 + (pos >= len(code)//2)
            else:
                steps = ((pos + 1 + (pos == 0) * len(code)) // 2 + (pos % 2 == 0) * (len(code) // 2 + 1)) % len(code)
            code = rotate(code, steps, True if not unscramble else False)

        elif line.startswith("move"):
            from_pos, to_pos = list(map(int, nums))[::direction]
            letter_to_insert = code[from_pos]
            code.remove(letter_to_insert)
            code.insert(to_pos, letter_to_insert)

        elif line.startswith("reverse"):
            start_pos, end_pos = map(int, nums)
            code = code[:start_pos] + code[start_pos:end_pos+1][::-1] + code[end_pos+1:]

    return ''.join(code)