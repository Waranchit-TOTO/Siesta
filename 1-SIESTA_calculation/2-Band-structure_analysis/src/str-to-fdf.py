import argparse
from pathlib import Path

from ase import io as ase_io
import sisl


SUPPORTED_EXTENSIONS = {".cif", ".vasp", ".xyz"}

ap = argparse.ArgumentParser(description="Convert .cif/.vasp/.xyz -> .xyz (ASE) -> .fdf (sisl)")
ap.add_argument("inputs", nargs="+", help="Input files or directories")
ap.add_argument("-o", "--output-dir", help="Output folder (default: input file folder)")
args = ap.parse_args()

out = Path(args.output_dir) if args.output_dir else None
if out:
	out.mkdir(parents=True, exist_ok=True)

files: list[Path] = []
for p in map(Path, args.inputs):
	if p.is_file():
		files.append(p)
	elif p.is_dir():
		files += [f for f in sorted(p.iterdir()) if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
	else:
		print(f"Skip (not found): {p}")

files = list(dict.fromkeys(files))
if not files:
	raise SystemExit("No input files found.")

ok = 0
for f in files:
	if f.suffix.lower() not in SUPPORTED_EXTENSIONS:
		continue
	try:
		d = out or f.parent
		xyz = d / f"{f.stem}.xyz"
		fdf = d / f"{f.stem}.fdf"
		ase_io.write(str(xyz), ase_io.read(str(f)))
		sisl.get_sile(str(xyz)).read_geometry().write(str(fdf))
		print(f"OK: {f} -> {xyz.name} -> {fdf.name}")
		ok += 1
	except Exception as e:
		print(f"Failed: {f} ({e})")

print(f"Done: {ok}/{len(files)} converted")