import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

import random as rd
import matplotlib

import sys






# compute color for each point
def compute_color(x,maxc,minc):
	if x > 0:
		return 0.5*x/max(maxc,abs(minc))
	if x < 0:
		return 0.5*x/max(maxc,abs(minc))
	return 0.0


# compute color for each point
def compute_log_color(x):
	return (1.0/(1.0 + np.exp(-100*x)) - 0.5)*2


def compute_linewidth(x):
	return 1.0 + 4.0*x

def plot_thickness(ts,metats):
	maxw = max(metats)
	# normalize the scores
	if maxw > 0:
		metats_norm = metats / maxw
	else:
		metats_norm = metats
	lwa = np.array([compute_linewidth(x) for x in metats_norm])
	
	# Create a color gradient from blue to red
	def compute_gradient_color(x):
		# x is normalized between 0 and 1
		# Blue (0, 0, 1) -> Red (1, 0, 0)
		return [x, 0, 1 - x]
	
	colormap = np.array([compute_gradient_color(x) for x in metats_norm])

	for i in range(0,len(ts)-1):
		lw = (lwa[i] + lwa[i+1])/2
		color = (colormap[i]+colormap[i+1])/2
		plt.plot([i,i+1],ts[i:(i+2)],linewidth = lw,c=color)


def plot_time_series_with_highlight(ts_file, scores_file, ith):

	o = abs(ith) - 1

	tss = open(ts_file,'r').readlines()
	scores = open(scores_file,'r').readlines()

	metats = np.array([float(x) for x in scores[o].strip().split(',')])
	# keep values based on the sign of the index
	if ith < 0:
		metats = -metats
	metats[metats < 0] = 0

	yts = np.array([float(x) for x in tss[o].strip().split(',')])
	y = int(yts[0])
	ts = yts[1:] # remove label

	plot_thickness(ts,metats)
	plt.title("Class " + str(y) + " - time series #" + str(o+1))
	return str(y)
	#plt.show()


# Example: python visual_timeseries.py ts.csv score.csv 2 -3
# will plot 2nd and 3rd time series from ts.csv with the highlight determined by score.csv
# the 2nd time series will be highlighted with postive score from score.csv and the 3rd time series highlighted with negative score

  
def visualize(ts_file_name, scores_file_name, indices):
	if (len(sys.argv) > 3):
		for ts in sys.argv[3:]:
			plt.figure(figsize=(20,10))
			label = plot_time_series_with_highlight(sys.argv[1] , sys.argv[2] ,int(ts))
			#plt.show()
			plt.savefig('figures/ts_highlights-' + str(int(ts)) + '-' + label + '.png', bbox_inches='tight')
	else:
		print("Need more input parameters")
  
if __name__ == "__main__":
	visualize(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]])
