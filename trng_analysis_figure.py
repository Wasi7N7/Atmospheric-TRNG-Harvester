import matplotlib.pyplot as plt
import numpy as np

# Load data
with open('quantum_data.txt', 'r') as f:
    bits = [int(b) for b in f.read().strip() if b in '01']

# Sample size for plotting
n_plot = 10000 
sample_bits = bits[:n_plot]

# Set scientific style
plt.style.use('seaborn-v0_8-muted')
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Statistical Analysis of Atmospheric Entropy Source', fontsize=16, fontweight='bold')

# --- 1. HISTOGRAM ---
axs[0].hist(bits, bins=[-0.5, 0.5, 1.5], rwidth=0.7, color='navy', edgecolor='black', alpha=0.8)
axs[0].set_xticks([0, 1])
axs[0].set_title('Bit Frequency Distribution')
axs[0].set_xlabel('Binary State')
axs[0].set_ylabel('Total Count')

# --- 2. TIME-DOMAIN WAVEFORM (First 100 bits) ---
axs[1].step(range(100), bits[:100], where='post', color='red', linewidth=1.5)
axs[1].set_ylim(-0.2, 1.2)
axs[1].set_title('Signal Waveform (t=0 to t=100)')
axs[1].set_xlabel('Bit Index (n)')
axs[1].set_ylabel('Logic Level')

# --- 3. 2D PHASE SPACE MAP ---
# Plotting bit[i] vs bit[i+1]
x = bits[:n_plot-1]
y = bits[1:n_plot]
# Adding slight "jitter" so points don't stack perfectly on (0,0), (0,1), etc.
x_jitter = x + np.random.normal(0, 0.05, len(x))
y_jitter = y + np.random.normal(0, 0.05, len(y))

axs[2].scatter(x_jitter, y_jitter, s=1, alpha=0.2, color='purple')
axs[2].set_title('2D Phase Space Map (Lag-1)')
axs[2].set_xlabel('Bit (n)')
axs[2].set_ylabel('Bit (n+1)')
axs[2].set_xticks([0, 1])
axs[2].set_yticks([0, 1])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('trng_analysis_figure.png', dpi=300)
print("[INFO] Scientific figure saved as trng_analysis_figure.png")
plt.show()