# binarysoup

An event‑driven, velocity‑conserving XOR interaction simulator in Python  
Tracks emergent “complexity” of bit‑string populations and their spatial interaction rates.

## Overview

**binarysoup** explores how a set of binary agents  
- each carrying an _n_-bit string  
- embedded in a _d_-dimensional space  
- moving only when they interact  
- exchanging and recombining bits via XOR  

can give rise to interesting dynamics in both information‐theoretic complexity and interaction frequency.

Two example scripts are provided:

- **`main.py`**  
  - A minimal m‑element pool (default m=50), purely XOR + mutation.  
  - Records Kolmogorov‐style complexity (via zlib/LZMA compression) over time.  
  - Outputs **`complexity_over_time.png`**.

- **`other.py`**  
  - A larger population (default m=900) in d=4 dimensions.  
  - Embeds bit‑strings → velocity via a block‐sum mapping.  
  - Conserves total momentum across interactions.  
  - Tracks both complexity _and_ interaction rate (fraction of sampled pairs that interact).  
  - Outputs **`plots.png`** with two stacked subplots.

## Features

- **Event‑driven**: No global tick—pick random pairs, decide interaction probabilistically based on distance.  
- **Velocity conservation**: Total vector sum of agent velocities stays constant, yet each agent’s velocity is driven by its own bit‑pattern.  
- **Complexity measurement**: Uses zlib & lzma to approximate Kolmogorov complexity of the entire bit‑population.  
- **Interaction‐rate tracking**: Monitors how spatial clustering (and bit‐driven velocities) influence how often XOR events occur.  
- **Configurable parameters**: Population size, bit‑length, embedding dimension, interaction radius (σ), mutation chance, record interval, etc.

## Getting Started

### Requirements

- Python 3.7+  
- `numpy`  
- `matplotlib`  
- (standard library) `random`, `zlib`, `lzma`

Install via pip if needed:

```bash
pip install numpy matplotlib
