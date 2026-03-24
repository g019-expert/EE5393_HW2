#!/usr/bin/env python3
"""
  RGB transfer: R1->G1->B1, R2->G2->B2 (each cycle)

  1/8 multiplier = three successive halvings (2C->C)
"""

import random

def halve(n):
    count = 0
    for _ in range(n):
        if random.random() < 0.5: # each molecule survives with prob 0.5
            count += 1
    return count

def one_eighth(n):
    return halve(halve(halve(n))) # n -> n/2 -> n/4 -> n/8

# one trial through all 5 cycles
def run_one_trial(inputs):
    B1, B2 = 0, 0
    outputs = []
    internals = []

    for x in inputs:
        # computation (blue-red phase)
        A = x + one_eighth(B1) + one_eighth(B2)
        C = one_eighth(B1) + one_eighth(B2)
        Y = one_eighth(A) + one_eighth(C)
        F = one_eighth(A)
        R1 = F
        H = one_eighth(x)
        E = one_eighth(B2)
        R2 = H + E

        outputs.append(Y)
        internals.append((A, C, F, H, E, R1, R2, B1, B2))

        # rgb transfer
        B1 = R1
        B2 = R2

    return outputs, internals

def main():
    inputs = [100, 5, 500, 20, 250]
    num_trials = 500

    all_y = [[] for _ in range(5)]
    all_R1 = [[] for _ in range(5)]
    all_R2 = [[] for _ in range(5)]

    for _ in range(num_trials):
        outs, ints = run_one_trial(inputs)
        for c in range(5):
            all_y[c].append(outs[c])
            all_R1[c].append(ints[c][5])
            all_R2[c].append(ints[c][6])

    # exact expected values
    B1e, B2e = 0.0, 0.0
    expected_y = []
    expected_r1 = []
    expected_r2 = []
    for x in inputs:
        Ae = x + B1e / 8.0 + B2e / 8.0
        Ce = B1e / 8.0 + B2e / 8.0
        Ye = Ae / 8.0 + Ce / 8.0
        R1e = Ae / 8.0
        R2e = x / 8.0 + B2e / 8.0
        expected_y.append(Ye)
        expected_r1.append(R1e)
        expected_r2.append(R2e)
        B1e = R1e
        B2e = R2e

    print(f"\n{'cycle':>6} | {'X':>6} | {'avg Y':>10} | {'expected':>10} | {'err':>6}")
    print("-" * 50)
    for c in range(5):
        avg_y = sum(all_y[c]) / len(all_y[c])
        print(f"{c+1:>6} | {inputs[c]:>6} | {avg_y:>10.2f} | {expected_y[c]:>10.2f} | {abs(avg_y - expected_y[c]):>6.2f}")

    print(f"\ndelay state averages:")
    print(f"{'cycle':>6} | {'avg R1':>10} | {'exp R1':>10} | {'avg R2':>10} | {'exp R2':>10}")
    print("-" * 60)
    for c in range(5):
        avg_r1 = sum(all_R1[c]) / len(all_R1[c])
        avg_r2 = sum(all_R2[c]) / len(all_R2[c])
        print(f"{c+1:>6} | {avg_r1:>10.2f} | {expected_r1[c]:>10.2f} | {avg_r2:>10.2f} | {expected_r2[c]:>10.2f}")


if __name__ == "__main__":
    main()
