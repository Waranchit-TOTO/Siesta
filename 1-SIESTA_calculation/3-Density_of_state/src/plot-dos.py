import numpy as np
import matplotlib.pyplot as plt

Ef = -6.5 # set your Fermi (eV) here
dos_file = "SnS2-band.DOS"


# -----------------------------
# Load spin-polarized DOS
# -----------------------------
def load_dos_spin(filename):
    data = np.loadtxt(filename)
    energy = data[:, 0] - Ef
    dos_up = data[:, 1]
    dos_dn = -data[:, 2]   # make spin-down negative
    return energy, dos_up, dos_dn

# -----------------------------
# Load files
# -----------------------------
E_tot, DOS_tot_up, DOS_tot_dn = load_dos_spin(dos_file)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))

# Total DOS
plt.plot(E_tot, DOS_tot_up, color="black", lw=2, label="Total up")
plt.plot(E_tot, DOS_tot_dn, color="black", lw=2, linestyle="--", label="Total down")

# -----------------------------
# Formatting
# -----------------------------
plt.axvline(0, color="gray", linestyle="--", linewidth=1)  # Fermi level

plt.xticks(size=20)
plt.yticks(size=20)

plt.xlim(-5,5)
plt.ylim(-8,8)

plt.title("Total Density of States", fontsize = 25)
plt.xlabel("Energy (eV)",  fontsize = 20)
plt.ylabel("DOS (states/eV)", fontsize = 20)
plt.legend(ncol=2, frameon=False, fontsize=15)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('total_dos.png')
plt.show()

