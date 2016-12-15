import re

def extended_gcd(a, b):
   x, y, u, v = 0, 1, 1, 0
   while b != 0:
       q, a, b = a // b, b, a % b
       x, u = u - q * x, x
       y, v = v - q * y, y
   return a, u, v

def modular_inverse(a, m):
   (g, x, y) = extended_gcd(a,m)
   if g != 1:
       raise ValueError("x (%d) and n (%d) are not coprime" % (a, m))
   return x % m

def chinese_remainder_theorem(vals, mods):
   m = 1
   x = 0
   for mod in mods:
       m *= mod
   for (m_i, a_i) in zip(mods, vals):
       M_i = m // m_i
       inv = modular_inverse(M_i, m_i)
       x = (x + a_i * M_i * inv) % m
   return x

def get_earliest_time(lines):
    values = []
    moduli = []
    for line in lines:
        disc, num_positions, at_time, cur_pos = map(int, re.findall(r"([\d]+)", line))
        values.append(-disc - (cur_pos - at_time) % num_positions)
        moduli.append(num_positions)
    return chinese_remainder_theorem(values, moduli)

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

print(get_earliest_time(lines)) #part 1 answer
lines.append("Disc #{} has {} positions; at time={}, it is at position {}.".format(len(lines) + 1, 11, 0, 0))
print(get_earliest_time(lines)) #part 2 answer