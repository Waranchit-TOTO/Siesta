import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def read_coop_cohp_data(filename):
    """
    Read COOP/COHP data file with format:
    #            ENERGY              s1              s2              total
    -31.21561292        0.00000112        0.00000112        0.00000224
    ...
    """
    data = []
    with open(filename, 'r') as f:
        for line in f:
            # Skip header lines starting with '#'
            if line.strip().startswith('#'):
                continue
            # Skip empty lines
            if not line.strip():
                continue
            # Parse data columns
            cols = line.split()
            if len(cols) >= 4:
                try:
                    energy = float(cols[0])
                    total = float(cols[3])
                    data.append([energy, total])
                except ValueError:
                    continue
    
    return np.array(data)

def plot_single(data, label, output_file='coop-cohp.png'):
    """
    Plot column 1 (ENERGY) vs column 4 (total) - single file
    """
    energy = data[:, 0]
    total = data[:, 1]
    
    plt.figure(figsize=(10, 6))
    plt.plot(energy, total, 'b-', linewidth=2, label=label)
    plt.xlabel('Energy (eV)', fontsize=12)
    plt.ylabel('COOP/COHP (Total)', fontsize=12)
    plt.title(f'COOP/COHP Analysis - {label}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved to {output_file}")
    plt.show()

def plot_multiple(files_dict, output_file='coop-cohp-combined.png'):
    """
    Plot multiple COOP/COHP files on the same figure
    files_dict: dictionary with {label: data_array}
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = ['b', 'r', 'g', 'm', 'c']
    
    for idx, (label, data) in enumerate(files_dict.items()):
        energy = data[:, 0]
        total = data[:, 1]
        color = colors[idx % len(colors)]
        
        # Plot on both axes
        ax1.plot(energy, total, color=color, linewidth=2, label=label)
        ax2.plot(energy, total, color=color, linewidth=2, label=label)
    
    # First subplot: normal view
    ax1.set_xlabel('Energy (eV)', fontsize=11)
    ax1.set_ylabel('COOP/COHP (Total)', fontsize=11)
    ax1.set_title('COOP/COHP Analysis - Normal View', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax1.legend(fontsize=10)
    
    # Second subplot: zoomed view around zero
    ax2.set_xlabel('Energy (eV)', fontsize=11)
    ax2.set_ylabel('COOP/COHP (Total)', fontsize=11)
    ax2.set_title('COOP/COHP Analysis - Zoomed View', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.set_ylim(-0.5, 0.5)  # Zoom around zero
    ax2.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Combined plot saved to {output_file}")
    plt.show()

# Main script execution
if len(sys.argv) < 2:
    print("Usage: python plot-coop-cohp.py <data_file> [output_file]")
    print("       python plot-coop-cohp.py --combine <file1> <file2> [output_file]")
    sys.exit(1)

if sys.argv[1] == '--combine':
    # Plot multiple files
    if len(sys.argv) < 4:
        print("Usage: python plot-coop-cohp.py --combine <file1> <file2> [output_file]")
        sys.exit(1)
    
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else 'coop-cohp-combined.png'
    
    if not os.path.exists(file1):
        print(f"Error: {file1} not found")
        sys.exit(1)
    if not os.path.exists(file2):
        print(f"Error: {file2} not found")
        sys.exit(1)
    
    data1 = read_coop_cohp_data(file1)
    data2 = read_coop_cohp_data(file2)
    
    if len(data1) > 0 and len(data2) > 0:
        label1 = os.path.basename(file1).replace('.mpr', '')
        label2 = os.path.basename(file2).replace('.mpr', '')
        files_dict = {label1: data1, label2: data2}
        plot_multiple(files_dict, output_file)
        print(f"Successfully plotted {len(data1)} and {len(data2)} data points")
    else:
        print("No data found in one or both files")
else:
    # Plot single file
    data_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'coop-cohp.png'
    
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found")
        sys.exit(1)
    
    data = read_coop_cohp_data(data_file)
    if len(data) > 0:
        label = os.path.basename(data_file).replace('.mpr', '')
        plot_single(data, label, output_file)
        print(f"Successfully plotted {len(data)} data points")
    else:
        print("No data found in file")
