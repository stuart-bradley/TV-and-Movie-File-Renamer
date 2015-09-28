"""
Batch renamer
Stuart Bradley
4/29/2014
"""

import os
import re
import shutil
import stat

test_loc = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Test_Structure").replace("\\","/")
test_loc_copy = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Test_Structure_copy").replace("\\","/")

files_to_change = ['.avi', '.mp4', '.mkv', '.srt'] 

mode = ''

title = ''
date = ''
season_ep = ''

# Changes Season folder names based on dirnames.
def change_seasons(dirnames, root):
	for d in dirnames:
		# Season is correctly named.
		if re.search("Season \d{1,2}", d):
			continue
		# Find season num.
		matchObj = re.search("S(\d{1,2})|Season.(\d{1,2})", d)
		# Get first non-empty match and strip leading zeroes.
		season_num = next(s for s in matchObj.groups() if s).lstrip('0')
		os.rename(os.path.join(root, d).replace("\\","/"), os.path.join(root, "Season " + season_num).replace("\\","/"))

########
# MAIN #
########

# Make a Copy of Test Structure
#shutil.copytree(test_loc, test_loc_copy)
#shutil.rmtree(test_loc)
#os.rename(test_loc_copy, test_loc)

for root, dirnames, filenames in os.walk(test_loc):
	# Set Root for WIN.
	root = root.replace("\\","/")
	# Determine main directory.
	if root.endswith("TV Shows"):
		mode = "TV"
	elif root.endswith("Movies"):
		mode = "Mo"

	if mode is "TV":
		# Check if in TV shows, and if inside a specific TV show. 
		matchObj = re.search("TV Shows\/([\w ]+$)",root)
		if not filenames and matchObj:
			# Set current Title.
			title = matchObj.group(1)
			# Set Season folder names.
			change_seasons(dirnames, root)
		# If inside a season (video files are present).
		if any(x.endswith(tuple(files_to_change)) for x in filenames):
			for f1 in filenames:
				# Video is correctly named.
				if re.search(" - S\d+(?:E\d+)+",f1):
					continue
				# Rename video, and subtitles.
				elif f1.endswith(tuple(files_to_change)):
					season_ep = re.search("(S\d+(?:E\d+)+)",f1).group(1)
					ext = f1.split(".")[-1]
					os.rename(os.path.join(root, f1).replace("\\","/"), os.path.join(root, (title +  " - " + season_ep + "." +ext)).replace("\\","/"))
				# Trash.
				else:
					os.remove(os.path.join(root, f1).replace("\\","/"))	
	elif mode is "Mo":
		if any(x.endswith(tuple(files_to_change)) for x in filenames):
			title = re.search("Movies\/([\w ]+\(\d{4}\)$)",root).group(1)
			for f1 in filenames:
				# Video is correctly named.
				if re.search("[\w ]+\(\d{4}\).\w+$",f1):
					continue
				# Rename video, and subtitles.
				elif f1.endswith(tuple(files_to_change)):
					ext = f1.split(".")[-1]
					os.rename(os.path.join(root, f1).replace("\\","/"), os.path.join(root, (title + "." +ext)).replace("\\","/"))
				# Trash.
				else:
					os.remove(os.path.join(root, f1).replace("\\","/"))