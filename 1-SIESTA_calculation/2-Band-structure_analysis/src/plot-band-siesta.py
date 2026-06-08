import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


plt.rcParams["font.family"] = "serif" #"Times New Roman"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["font.weight"] = "bold"


def read_bands_file(filepath):
    """
    Read Siesta bands file in Gnuplot format.
    Format: k-points in first column, energies in second column, band index in third column
    Bands are separated by blank lines.
    """
    bands_dict = {}
    current_band = None
    k_points = []
    energies = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and header
            if not line or line.startswith('#'):
                continue
            
            # Parse data line
            parts = line.split()
            if len(parts) >= 3:
                k = float(parts[0])
                E = float(parts[1])
                band_idx = int(parts[2])
                
                # If this is a new band or first data point
                if band_idx not in bands_dict:
                    bands_dict[band_idx] = {'k': [], 'E': []}
                
                bands_dict[band_idx]['k'].append(k)
                bands_dict[band_idx]['E'].append(E)
    
    return bands_dict


def plot_band_structure(bands_dict, k_labels=None, output_file='band_structure-siesta.png', plot_type='line'):
    """
    Plot band structure from the bands dictionary.
    
    Parameters:
    -----------
    bands_dict : dict
        Dictionary of bands with k-points and energies
    k_labels : list of tuples, optional
        List of (k_value, label_name) for high-symmetry points
    output_file : str
        Output filename for the plot
    plot_type : str
        'line' for line plot or 'scatter' for scatter plot
    """
    fig, ax = plt.subplots(figsize=(4.2, 8))
    
    # Plot each band
    for band_idx, data in sorted(bands_dict.items()):
        k_points = np.array(data['k'])
        energies = np.array(data['E'])
        
        if plot_type == 'scatter':
            #ax.scatter(k_points, energies - (-6.013815), s=20, alpha=0.8, color='b', marker = '.')
            ax.scatter(k_points, energies , s=20, alpha=0.8, color='b', marker = '.')
        else:  # line plot
            ax.plot(k_points, energies, 'b:', linewidth=0.5, alpha=0.7)
    
    # Add high-symmetry k-point labels and vertical lines
    if k_labels:
        k_values = [label[0] for label in k_labels]
        k_names = [label[1] for label in k_labels]
        
        # Add vertical lines at high-symmetry points
        for k_val in k_values:
            ax.axvline(x=k_val, color='black', linestyle='-', linewidth=2, alpha=1)
        
        # Set x-axis ticks and labels
        ax.set_xticks(k_values)
        ax.set_xticklabels(k_names, fontsize=16)
    
    # Formatting
    ax.axhline(y=0, color='r', linestyle='--', linewidth=1, label='Fermi level (E=0)')
#    ax.axhline(y=0.5, color='black', linestyle='-', linewidth=1 ) #, label='')
#    ax.axhline(y= -0.5, color='black', linestyle='-', linewidth=1 ) #, label='')
    ax.set_ylim(-10,10)
    ax.set_xlim(0, 2.274012)
    ax.tick_params(axis='y', labelsize=16)
#    ax.set_xlabel('k-point path', fontsize=12)
#    ax.set_ylabel('Energy (eV)', fontsize=12)
    ax.set_title('Band Structure, Siesta', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
#    ax.legend()
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Band structure plot saved to {output_file}")
    plt.show()


# Read and plot band structure
bands_file = Path('bands')

# Define high-symmetry k-points

k_labels = [
    (0.000000, '${/GAMMA}$'),
    (0.541363, '$Y$'),
    (0.684956, '$T$'),
    (1.226319, '$Z$'),   
    (1.786469, '$S$'),
    (1.930062, '$R$'),
    (2.274012, '${/SIGMA_0}$'),
    (2.899098, '$C_0$'),
    (3.540465, '$A_0$'),
    (4.165551, '$E_0$')
    ]

if bands_file.exists():
    bands_dict = read_bands_file(bands_file)
    print(f"Successfully loaded {len(bands_dict)} bands from {bands_file}")
    # Change plot_type to 'scatter' or 'line'
    plot_band_structure(bands_dict, k_labels=k_labels, plot_type='scatter')
else:
    print(f"Error: {bands_file} not found!")