from Scrambler import scrambler
from RandomInstructionsCreator import random_instructions_creator
from string import ascii_lowercase

def test(max_len_string=26, num_trials_per_string=100, num_instructions=100):
    for len_string in range(4, max_len_string + 1, 2):
        input_string = ascii_lowercase[:len_string]
        print("Performing tests for input string \"{}\"...".format(input_string))
        for trial in range(num_trials_per_string):
            instructions = random_instructions_creator(input_string, num_instructions)
            scrambled = scrambler(input_string, instructions)
            descrambled = scrambler(scrambled, instructions, True)
            if descrambled != input_string:
                print("Input string \"{}\" scrambled to \"{}\" but descrambled to \"{}\""
                      .format(input_string, scrambled, descrambled))
                print("Instructions: ", instructions)
                return False
    return True

print(test())