import re

def egcd(a, b):
   x, y, u, v = 0, 1, 1, 0
   while b != 0:
       q, a, b = a // b, b, a % b
       x, u = u - q * x, x
       y, v = v - q * y, y
   return a, u, v

def inverse(a, m):
   (g, x, y) = egcd(a,m)
   if g != 1:
       raise ValueError("x (%d) and n (%d) are not coprime" % (a, m))
   return x % m

def crt(vals, mods):
   m = 1
   x = 0
   for mod in mods:
       m *= mod
   for (m_i, a_i) in zip(mods, vals):
       M_i = m // m_i
       inv = inverse(M_i, m_i)
       x = (x + a_i * M_i * inv) % m
   return x

DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")
values = []
moduli = []

for line in lines:
    disc, num_positions, at_time, cur_pos = map(int, re.findall(r"([\d]+)", line))
    values.append(-disc - (cur_pos - at_time) % num_positions)
    moduli.append(num_positions)

print(crt(values, moduli)) #part 1 answer
values.append(-(len(values) + 1))
moduli.append(11)
print(crt(values, moduli)) #part 2 answer