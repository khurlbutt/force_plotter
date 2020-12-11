"""
File: force_plotter.py
----------------------
Kevin Hurlbutt
2020-12-11

In DFT calculations within VASP, monitoring convergence is simple for the 
electronic steps, since the change in energy is printed after every electronic 
step. However, it is more difficult to monitor the convergence of the ionic 
optimization if a force criterion, instead of a total energy criterion, is 
used. This program plots all the forces as an animated bar plot so one can 
watch as the structure approaches equilirbium.

This script plots the forces on ions at each step in a geometry optimization 
as calculated by VASP. If launched from the same directory as a VASP OUTCAR 
file, it will animate the forces (in each direction). It depends on the 
library "matplotlib".
"""
# import statements
import matplotlib
matplotlib.rcParams['font.sans-serif'] = 'Arial'
matplotlib.rcParams['font.size'] = 12
import matplotlib.pyplot as plt

class ForcePlotter():
	"""This wraps the whole class."""
	def __init__(self, input_file="./OUTCAR"):
		self.INPUT_FILE = input_file	# path to the OUTCAR file
		self.CUTOFF = 0.05				# this will plot a dashed red line at the EDIFFG force
		self.PAUSE_LENGTH = 0.1			# 1 / framerate, in seconds
		self.all_forces = []			# all the forces as a list
		self.y_range = [-0.1, 0.1]		# y range to plot

	def run(self):
		# this reads in the forces and plots the values
		with open(self.INPUT_FILE, encoding="utf8", errors="ignore") as f:
			for line in f:
				if "TOTAL" in line:
					forces = []
					line = f.readline()
					line = f.readline()
					while "---" not in line:
						parts = line.split()
						forces.append(float(parts[3]))
						forces.append(float(parts[4]))
						forces.append(float(parts[5]))
						line = f.readline()
					self.all_forces.append(forces)
		f.close()
		step = 0
		for forces in self.all_forces:
			step += 1
			fig, ax = plt.subplots(figsize=(13.33, 6.5))
			ax.bar(range(len(forces)), forces, color="black")
			ax.set_ylim(self.y_range)
			ax.set_ylabel("Force / eV $\AA^{-1}$")
			ax.set_xticks([])
			ax.set_title("Ionic-step number "+str(step))
			ax.plot([0,len(forces)+1],[self.CUTOFF, self.CUTOFF], color="red", linestyle="--")
			ax.plot([0,len(forces)+1],[-self.CUTOFF, -self.CUTOFF], color="red", linestyle="--")
			plt.tight_layout()
			plt.pause(self.PAUSE_LENGTH)

def main():
	input_file = "./OUTPUT"
	f = ForcePlotter()
	f.run()

if __name__ == '__main__':
	main()
