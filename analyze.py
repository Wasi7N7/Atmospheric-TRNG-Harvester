import math
import sys
import os
from collections import Counter

# --- CONFIGURATION ---
INPUT_FILE = "quantum_data.txt"
SIGNIFICANCE_LEVEL = 0.01  # Alpha = 0.01 (99% Confidence Interval)

def load_data(filepath):
    """Loads raw binary data from file."""
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        sys.exit(1)
    
    with open(filepath, 'r') as f:
        raw = f.read().strip()
    
    # Filter non-binary characters
    bits = [int(b) for b in raw if b in '01']
    return bits

def calculate_entropy(bits):
    """Calculates Shannon Entropy in bits per bit."""
    n = len(bits)
    if n == 0: return 0.0
    
    counts = Counter(bits)
    p0 = counts[0] / n
    p1 = counts[1] / n
    
    entropy = 0.0
    if p0 > 0: entropy -= p0 * math.log2(p0)
    if p1 > 0: entropy -= p1 * math.log2(p1)
    
    return entropy

def monobit_test(bits):
    """
    Performs the NIST Frequency (Monobit) Test.
    H0: The sequence is random.
    """
    n = len(bits)
    s_n = sum(1 if b == 1 else -1 for b in bits)
    s_obs = abs(s_n) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def chi_squared_test(bits):
    """
    Performs Pearson's Chi-Squared Test for Uniformity.
    """
    n = len(bits)
    observed_zeros = bits.count(0)
    observed_ones = bits.count(1)
    expected = n / 2
    
    chi_sq = ((observed_zeros - expected) ** 2 / expected) + \
             ((observed_ones - expected) ** 2 / expected)
    
    return chi_sq

def serial_correlation(bits):
    """
    Calculates the Serial Correlation Coefficient (Lag-1).
    Measures dependence between bit[i] and bit[i+1].
    """
    n = len(bits)
    if n < 2: return 0.0
    
    # Calculate mean and variance
    mean = sum(bits) / n
    variance = sum((b - mean) ** 2 for b in bits) / n
    
    # Calculate covariance
    covariance = sum((bits[i] - mean) * (bits[i+1] - mean) for i in range(n-1)) / (n-1)
    
    if variance == 0: return 0.0
    return covariance / variance

def run_audit():
    print("================================================================")
    print("   STOCHASTIC SIGNAL ANALYSIS REPORT: ATMOSPHERIC TRNG SOURCE   ")
    print("================================================================")
    
    # 1. Data Acquisition
    print(f"[INFO] Loading dataset: {INPUT_FILE}")
    bits = load_data(INPUT_FILE)
    n = len(bits)
    print(f"[DATA] Total Samples (N): {n:,} bits")
    
    if n < 1000:
        print("[WARNING] Sample size insufficient for statistical significance.")
    
    print("-" * 64)
    
    # 2. Shannon Entropy
    print("TEST 1: SHANNON ENTROPY (Information Density)")
    entropy = calculate_entropy(bits)
    print(f"   > Theoretical Max: 1.00000000")
    print(f"   > Calculated:      {entropy:.8f}")
    print(f"   > Efficiency:      {(entropy/1.0)*100:.6f}%")
    
    # 3. Monobit Frequency Test (NIST SP 800-22)
    print("-" * 64)
    print("TEST 2: FREQUENCY (MONOBIT) TEST")
    print("   > Null Hypothesis (H0): Distribution is uniform.")
    
    ones = sum(bits)
    zeros = n - ones
    proportion = ones / n
    
    p_value = monobit_test(bits)
    
    print(f"   > Zero Count:      {zeros:,} ({zeros/n:.4%})")
    print(f"   > One Count:       {ones:,} ({ones/n:.4%})")
    print(f"   > Delta (Bias):    {abs(ones-zeros):,} bits")
    print(f"   > P-Value:         {p_value:.6f}")
    
    if p_value >= SIGNIFICANCE_LEVEL:
        print(f"   > Conclusion:      PASS (Fail to Reject H0 at alpha={SIGNIFICANCE_LEVEL})")
    else:
        print(f"   > Conclusion:      FAIL (Reject H0 - Evidence of Bias)")

    # 4. Chi-Squared Test
    print("-" * 64)
    print("TEST 3: PEARSON'S CHI-SQUARED TEST")
    chi_sq = chi_squared_test(bits)
    # Critical value for 1 degree of freedom at alpha=0.01 is 6.635
    critical_val = 6.635 
    
    print(f"   > Chi^2 Statistic: {chi_sq:.4f}")
    print(f"   > Critical Value:  {critical_val} (alpha=0.01)")
    
    if chi_sq < critical_val:
        print("   > Conclusion:      PASS (Consistent with Uniform Distribution)")
    else:
        print("   > Conclusion:      FAIL (Deviates from Uniformity)")

    # 5. Serial Correlation
    print("-" * 64)
    print("TEST 4: SERIAL CORRELATION (Lag-1)")
    print("   > Objective: Detect periodic patterns or 50Hz interference.")
    
    corr = serial_correlation(bits)
    print(f"   > Coefficient:     {corr:.6f}")
    
    # Ideal correlation is 0. Threshold set to +/- 0.01 for high quality.
    if abs(corr) < 0.01:
        print("   > Conclusion:      NEGLIGIBLE (Independent Samples)")
    elif abs(corr) < 0.05:
        print("   > Conclusion:      LOW (Minor Dependencies Detected)")
    else:
        print("   > Conclusion:      HIGH (Significant Auto-Correlation Detected)")

    print("================================================================")
    print("END OF REPORT")
    print("================================================================")

if __name__ == "__main__":
    run_audit()