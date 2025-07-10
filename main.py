import random
import zlib
import lzma
import matplotlib.pyplot as plt

m = 50      # of elements
l = 64       # length of binary string of each element 
iterations = 100000
record_interval = 10
flip_chance = 0.9

def maybe_flip_random_bit(bitstring, chance=0.5):
    if random.random() < chance:
        idx = random.randint(0, len(bitstring) - 1)
        bitstring[idx] ^= 1  # flip the bit
    return bitstring

def pack_bits(bits):
    byte_arr = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte |= (bits[i + j] << (7 - j))
        byte_arr.append(byte)
    return bytes(byte_arr)

bitstrings = [[random.randint(0, 1) for _ in range(l)] for _ in range(m)]

iterations_recorded = []
complexities = []

for it in range(1, iterations + 1):
    i, j = random.sample(range(m), 2)
    A = bitstrings[i]
    B = bitstrings[j]
    
    C = [a ^ b for a, b in zip(A, B)]
    
    pool = [A, B, C]
    newA = random.choice(pool)
    pool_excl_A = [x for x in pool if x is not newA]
    newB = random.choice(pool_excl_A)
    
    newA = maybe_flip_random_bit(newA, flip_chance)
    newB = maybe_flip_random_bit(newB, flip_chance)
    bitstrings[i] = newA.copy()
    bitstrings[j] = newB.copy()
    
    if it % record_interval == 0:
        # flatten bits
        flat_bits = [bit for bs in bitstrings for bit in bs]
        bit_bytes = pack_bits(flat_bits)
        # compress and record minimum size
        zlib_size = len(zlib.compress(bit_bytes))
        lzma_size = len(lzma.compress(bit_bytes))
        complexities.append(min(zlib_size, lzma_size))
        iterations_recorded.append(it)

plt.figure()
plt.plot(iterations_recorded, complexities)
plt.xlabel('Iteration')
plt.ylabel('Approx. Kolmogorov Complexity (bytes)')
plt.title('Complexity Over Time in XOR Interaction Simulation')

filename = 'complexity_over_time.png'
plt.savefig(filename)
plt.close()

print(f"Plot saved to: {filename}")
