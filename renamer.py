"""
Batch renamer
Stuart Bradley
4/29/2014
"""

import os
import re

test_loc = "/home/stuart/Code/Renamer/Test Structure"

files_to_change = ['.avi', '.mp4', '.mkv'] 

def change_seasons(dirnames):
	for d in dirnames:
		if re.search("Season \d{1,2}", d):
			continue
		# Find season num.
		matchObj = re.search("S(\d{1,2})|Season.(\d{1,2})", d)
		# Get first non-empty match and strip leading zeroes.
		season_num = next(s for s in matchObj.groups() if s).lstrip('0')
		os.rename(os.path.join(root, d), os.path.join(root, "Season " + season_num))



for root, dirnames, filenames in os.walk(test_loc):
	title = ''
	date = ''
	season_ep = ''
	# Check if in TV shows, and if inside a specific TV show. 
	matchObj = re.search("TV Shows\/([\w ]+$)",root)
	if not filenames and matchObj:
		title = matchObj.group(1)
		change_seasons(dirnames)
	if any(x.endswith(tuple(files_to_change)) for x in filenames):
		continue