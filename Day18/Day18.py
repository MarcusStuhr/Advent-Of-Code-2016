TRAP = '^'
SAFE = '.'
DATA_FILENAME = "data.txt"

def count_safe_tiles_grid(first_row, num_rows):
    num_safe_tiles = first_row.count(SAFE)
    prev_row = SAFE + first_row + SAFE
    for row_index in range(num_rows - 1):
        new_row = ""
        for col_index in range(1, len(prev_row) - 1):
            if prev_row[col_index - 1] == prev_row[col_index + 1]:
                num_safe_tiles += 1
                new_row += SAFE
            else:
                new_row += TRAP
        prev_row = SAFE + new_row + SAFE
    return num_safe_tiles


first_row = open(DATA_FILENAME).read().split("\n")[0]
print(count_safe_tiles_grid(first_row, 40))
first_row = open(DATA_FILENAME).read().split("\n")[0]
print(count_safe_tiles_grid(first_row, 400000))