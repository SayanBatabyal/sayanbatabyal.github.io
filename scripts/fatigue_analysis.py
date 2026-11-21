"""
Author: Sayan Batabyal
Date: 2026-11-22
Purpose: Analyze a stress-history CSV using hysteresis and peak-valley filtering,
simplified cycle counting, and the Basquin/Palmgren-Miner fatigue damage method.
"""

import numpy as np
import pandas as pd
import argparse

def hysteresis_filter(signal, threshold):
    """Removes small fluctuations smaller than the threshold"""
    if len(signal) == 0:
        return np.array([])
    filtered = [signal[0]]
    for value in signal[1:]:
        if abs(value - filtered[-1]) >= threshold:
            filtered.append(value)
    return np.array(filtered)

def peak_valley_filter(signal):
    """Keeps only local maxima and minima, removing intermediate points"""
    if len(signal) < 3:
        return np.array(signal)
    filtered = [signal[0]]
    for i in range(1, len(signal) - 1):
        prev_val, curr_val, next_val = signal[i-1], signal[i], signal[i+1]
        if (curr_val > prev_val and curr_val > next_val) or (curr_val < prev_val and curr_val < next_val):
            filtered.append(curr_val)
    filtered.append(signal[-1])
    return np.array(filtered)

def analyze_fatigue(stress_history, time_history=None, threshold=10.0, m=3.0, C=2.0e11):
    """
    Executes the entire fatigue analysis workflow:
      1. Hysteresis filtering
      2. Peak-Valley filtering
      3. Simplified cycle counting with time tracking
      4. Cumulative fatigue damage calculation using Palmgren-Miner's rule and Basquin relation.
    """
    stress_history = np.asarray(stress_history)
    if time_history is None:
        time_history = np.arange(len(stress_history))
    else:
        time_history = np.asarray(time_history)
        
    # Step 1: Hysteresis Filtering
    filtered_hyst = hysteresis_filter(stress_history, threshold=threshold)
    
    # Step 2: Peak-Valley Filtering
    filtered_pv = peak_valley_filter(filtered_hyst)
    
    # Reconstruct original indices for time-tracking
    filtered_pv_orig_indices = []
    curr_idx = 0
    for val in filtered_pv:
        for idx in range(curr_idx, len(stress_history)):
            if np.isclose(stress_history[idx], val):
                filtered_pv_orig_indices.append(idx)
                curr_idx = idx + 1
                break
                
    # Prepare tracking info: (value, original_index, original_time)
    indexed_points = [
        (filtered_pv[i], filtered_pv_orig_indices[i], time_history[filtered_pv_orig_indices[i]]) 
        for i in range(len(filtered_pv))
    ]
    
    results = []
    cycle_id = 1
    
    # Step 3: Cycle Counting and Damage Tracking
    while len(indexed_points) >= 3:
        i = 0
        cycle_found = False
        while i < len(indexed_points) - 2:
            range1 = abs(indexed_points[i+1][0] - indexed_points[i][0])
            range2 = abs(indexed_points[i+2][0] - indexed_points[i+1][0])
            
            if range2 >= range1:
                p1 = indexed_points[i]
                p2 = indexed_points[i+1]
                
                if p1[0] >= p2[0]:
                    max_pt, min_pt = p1, p2
                else:
                    max_pt, min_pt = p2, p1
                    
                s_range = range1
                N_f = C / (s_range ** m) if s_range > 0 else float('inf')
                damage = 1.0 / N_f if N_f != float('inf') else 0.0
                
                results.append({
                    "Cycle ID": cycle_id,
                    "Min Stress Index": min_pt[1],
                    "Min Time Point": round(min_pt[2], 4),
                    "Min Stress (MPa)": round(min_pt[0], 2),
                    "Max Stress Index": max_pt[1],
                    "Max Time Point": round(max_pt[2], 4),
                    "Max Stress (MPa)": round(max_pt[0], 2),
                    "Stress Range (MPa)": round(s_range, 2),
                    "Allowable Cycles (N_f)": int(N_f) if N_f != float('inf') else "Infinite",
                    "Damage Contribution (D_i)": damage
                })
                
                cycle_id += 1
                indexed_points.pop(i+1)
                indexed_points.pop(i)
                cycle_found = True
                break
            else:
                i += 1
        if not cycle_found:
            break
            
    damage_df = pd.DataFrame(results)
    total_damage = damage_df["Damage Contribution (D_i)"].sum() if not damage_df.empty else 0.0
    
    return total_damage, damage_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Compute cumulative fatigue damage from a stress dataset CSV.")
    parser.add_argument('csv_path', type=str, help="Path to the CSV dataset.")
    parser.add_argument('--stress_col', type=str, default='stress', help="Name of the column containing stress values.")
    parser.add_argument('--time_col', type=str, default=None, help="Optional column containing time steps.")
    parser.add_argument('--threshold', type=float, default=10.0, help="Hysteresis filter threshold.")
    parser.add_argument('--m', type=float, default=3.0, help="S-N fatigue exponent.")
    parser.add_argument('--C', type=float, default=2.0e11, help="S-N material constant.")
    parser.add_argument('--output_cycles', type=str, default=None, help="Optional CSV file to save counted cycles.")
    
    args = parser.parse_args()
    
    df = pd.read_csv(args.csv_path)
    stresses = df[args.stress_col].values
    times = df[args.time_col].values if args.time_col else None
    
    tot_dmg, cycles_df = analyze_fatigue(
        stress_history=stresses,
        time_history=times,
        threshold=args.threshold,
        m=args.m,
        C=args.C
    )
    
    print(f"Total Cumulative Fatigue Damage (D): {tot_dmg:.3e}")
    if tot_dmg > 0:
        print(f"Estimated fatigue life: {1.0 / tot_dmg:,.0f} duration-units")
        
    if args.output_cycles:
        cycles_df.to_csv(args.output_cycles, index=False)
        print(f"Saved counted cycle details to {args.output_cycles}")
