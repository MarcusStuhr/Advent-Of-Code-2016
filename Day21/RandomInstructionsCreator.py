from random import randint, sample

def random_instructions_creator(input_string, num_instructions):

    if len(set(input_string)) != len(input_string):
        raise Exception("Input string \"{}\" invalid: All characters must be unique.".format(input_string))

    possible_instructions = ["swap position <int> with position <int>",
                             "swap letter <char> with letter <char>",
                             "reverse positions <ord_int> through <ord_int>",
                             "rotate left <int> steps",
                             "rotate right <int> steps",
                             "move position <int> to position <int>",
                             "rotate based on position of letter <char>"]

    instructions = []

    for num_instruction in range(num_instructions):
        instruction = possible_instructions[randint(0, len(possible_instructions)) - 1]
        unique_ints = sample(range(0, len(input_string)), instruction.count("<int>"))
        unique_ord_ints = sample(range(0, len(input_string)), instruction.count("<ord_int>"))
        unique_chars = sample(input_string, instruction.count("<char>"))

        for num in unique_ints:
            instruction = instruction.replace("<int>", str(num), 1)

        for num in sorted(unique_ord_ints):
            instruction = instruction.replace("<ord_int>", str(num), 1)

        for char in unique_chars:
            instruction = instruction.replace("<char>", char, 1)

        if instruction.endswith("steps") and len(unique_ints) == 1:
            instruction = instruction[:-1] #"..."steps" -> "...step"

        instructions.append(instruction)

    return instructions


instructions = random_instructions_creator("abcdefgh", 100)
print('\n'.join(instructions))