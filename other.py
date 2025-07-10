import random
import zlib
import lzma
import matplotlib.pyplot as plt
import numpy as np
m = 900         # number of agents
l = 64         # length of binary string
d = 4          # embedding dimension
iterations = 100000
record_interval = 100
flip_chance = 0.5
sigma = 0.5    # interaction distance scale

def g(block_bits, d=d):
    """
    Simple block‑sum mapping: split the l‑bit string into d blocks
    and return a length‑d array of the sums of each block.
    """
    block_size = len(block_bits) // d
    vec = np.zeros(d)
    for k in range(d):
        start = k * block_size
        end   = start + block_size
        vec[k] = sum(block_bits[start:end])
    return vec
def maybe_flip_random_bit(bitstring, chance=0.5):
    if random.random() < chance:
        idx = random.randrange(len(bitstring))
        bitstring[idx] ^= 1
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
positions = np.random.rand(m, d)

total_trials      = 0
successful_hits   = 0
interaction_rates = []

velocities = np.vstack([ g(bs) for bs in bitstrings ])
velocities -= velocities.mean(axis=0)
iterations_recorded = []
complexities = []
for it in range(1, iterations + 1):
    # pick two distinct agents
    i, j = random.sample(range(m), 2)
    total_trials += 1
    dist = np.linalg.norm(positions[i] - positions[j])
    p_int = np.exp(- (dist**2) / (2 * sigma**2))
    if random.random() < p_int:
         
        successful_hits += 1

        positions[i] += velocities[i]
        positions[j] += velocities[j]
        
        # XOR interaction
        A = bitstrings[i]
        B = bitstrings[j]
        C = [a ^ b for a, b in zip(A, B)]
        # choose two non-zero outcomes
        pool = [A, B, C]
        pool = [x for x in pool if any(x)]  # discard zero-string
        newA, newB = random.sample(pool, 2)
        
        # optional bit-flip mutation
        newA = maybe_flip_random_bit(newA.copy(), flip_chance)
        newB = maybe_flip_random_bit(newB.copy(), flip_chance)
            
        # assign new bitstrings
        bitstrings[i] = newA
        bitstrings[j] = newB

        # recompute velocities from the updated bits
        velocities[i] = g(newA)
        velocities[j] = g(newB)

        # enforce global momentum conservation
        drift = velocities.mean(axis=0)
        velocities -= drift
    
    # record complexity at intervals
    if it % record_interval == 0:
        rate = successful_hits / total_trials
        interaction_rates.append(rate)
        total_trials = 0
        successful_hits = 0
        flat_bits = [bit for bs in bitstrings for bit in bs]
        bit_bytes = pack_bits(flat_bits)
        zlib_size = len(zlib.compress(bit_bytes))
        lzma_size = len(lzma.compress(bit_bytes))
        complexities.append(min(zlib_size, lzma_size))
        iterations_recorded.append(it)


output_filename = 'plots.png'

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

# Top: complexity
ax1.plot(iterations_recorded, complexities)
ax1.set_ylabel('Complexity (bytes)')
ax1.set_title('Complexity Over Time')
minc, maxc = min(complexities), max(complexities)
rng_c = maxc - minc
if rng_c < 1e-6:
    # flat data → give ±1 byte of padding
    ax1.set_ylim(minc - 1, maxc + 1)
else:
    padc = 0.05 * rng_c
    ax1.set_ylim(minc - padc, maxc + padc)

# Bottom: interaction rate
ax2.plot(iterations_recorded, interaction_rates)
ax2.set_xlabel('Iteration')
ax2.set_ylabel('Interaction Rate')
ax2.set_title('Interaction Rate Over Time')
mini, maxi = min(interaction_rates), max(interaction_rates)
rng_r = maxi - mini
if rng_r < 1e-6:
    # almost zero data → show 0–0.25
    ax2.set_ylim(0, 0.25)
else:
    padi = 0.05 * rng_r
    ax2.set_ylim(mini - padi, maxi + padi)

plt.tight_layout()
plt.savefig(output_filename)
plt.close()

print(f"Plot saved to: {output_filename}")
