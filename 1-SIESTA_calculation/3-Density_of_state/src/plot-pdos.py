import numpy as np
import matplotlib.pyplot as plt

Ef = -6.5 # set your Fermi (eV) here
dos_file = "SnS2-band.DOS"

Sn_dos = "Sn_dos.dat"
S_dos = "S_dos.dat"

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
E_Sn, DOS_Sn_up, DOS_Sn_dn = load_dos_spin(Sn_dos)
E_S, DOS_S_up, DOS_S_dn = load_dos_spin(S_dos)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(8, 5))

# Total DOS
plt.plot(E_tot, DOS_tot_up, color="black", lw=2, label="Total up")
plt.plot(E_tot, DOS_tot_dn, color="black", lw=2, linestyle="--", label="Total down")

# PDOS
plt.plot(E_Sn, DOS_Sn_up, color="blue", lw=2, label="Sn up")
plt.plot(E_Sn, DOS_Sn_dn, color="blue", lw=2, linestyle="--", label="Sn down")
plt.plot(E_S, DOS_S_up, color="red", lw=2, label="S up")
plt.plot(E_S, DOS_S_dn, color="red", lw=2, linestyle="--", label="S down")

# -----------------------------
# Formatting
# -----------------------------
plt.axvline(0, color="gray", linestyle="--", linewidth=1)  # Fermi level

plt.xticks(size=20)
plt.yticks(size=20)

plt.xlim(-5,5)
plt.ylim(-8,8)

plt.title("Projected Density of States", fontsize = 25)
plt.xlabel("Energy (eV)",  fontsize = 20)
plt.ylabel("DOS (states/eV)", fontsize = 20)
plt.legend(ncol=2, frameon=False, fontsize=15)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('projected_dos.png')
plt.show()

